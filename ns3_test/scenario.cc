/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2009 The Boeing Company
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

//written by 김진아, 2020
#include "ns3/command-line.h"
#include "ns3/netanim-module.h"
#include "ns3/config.h"
#include "ns3/double.h"
#include "ns3/string.h"
#include "ns3/log.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/ipv4-address-helper.h"
#include "ns3/yans-wifi-channel.h"
#include "ns3/mobility-model.h"
#include "ns3/internet-stack-helper.h"
#include "ns3/snr-tag.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("WifiSimpleAdhoc");

//by 김진아, log Tx address and rss
void txTrace(Ptr<const Packet> packet,uint16_t channelFreqMhz,WifiTxVector txVector,MpduInfo aMpdu){
	
 // SetPosition();
  
  std::ofstream outFile;
  outFile.open("scenario3.txt",std::ios_base::out |std::ios_base::app);
 
  outFile<<"Tx time: "<<Simulator::Now().GetSeconds()<<", Node: "<<Simulator::GetContext()<<std::endl;
  outFile.close();
}


//by 김진아, log Rx address and rss
void rxTrace(Ptr<const Packet> packet,uint16_t channelFreqMhz,WifiTxVector txVector,MpduInfo aMpdu,SignalNoiseDbm signalNoise){
	
  std::ofstream outFile;
  outFile.open("scenario3.txt",std::ios_base::out| std::ios_base::app);     
  
  outFile<<"Rx time: "<<Simulator::Now().GetSeconds()<<", Node: "<<Simulator::GetContext()<<", rss: "<<signalNoise.signal<<std::endl;
  outFile.close();
  
}


static void GenerateTraffic (Ptr<Socket> socket, uint32_t pktSize,
                             uint32_t pktCount, Time pktInterval )
{
  if (pktCount > 0)
    {
      socket->Send (Create<Packet> (pktSize));
      Simulator::Schedule (pktInterval, &GenerateTraffic,
                           socket, pktSize,pktCount , pktInterval);
    }
  else
    {
      socket->Close ();
    }
}


static void CourseChange (std::string foo, Ptr<const MobilityModel> mobility)
{
  Vector pos = mobility->GetPosition ();

  std::ofstream outFile;
   outFile.open("scenario3.txt",std::ios_base::out |std::ios_base::app);

   outFile<<"Changed Pos" <<" x="<<pos.x<<", y="<<pos.y<<", z=:"<<pos.z<<std::endl;

}

int main (int argc, char *argv[])
{
  std::string phyMode ("DsssRate1Mbps");
  uint32_t packetSize = 1000; // bytes
  uint32_t numPackets = 1;
  double interval = 1.0; // seconds

  CommandLine cmd;
  cmd.AddValue ("phyMode", "Wifi Phy mode", phyMode);
  cmd.AddValue ("packetSize", "size of application packet sent", packetSize);
  cmd.AddValue ("numPackets", "number of packets generated", numPackets);
  cmd.AddValue ("interval", "interval (seconds) between packets", interval);
  cmd.Parse (argc, argv);

  Time interPacketInterval = Seconds (interval);

  Config::SetDefault ("ns3::WifiRemoteStationManager::NonUnicastMode",StringValue (phyMode));

  NodeContainer c;
  c.Create (5);

  WifiHelper wifi;
  wifi.SetStandard (WIFI_PHY_STANDARD_80211b);
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
                                "DataMode",StringValue (phyMode),
                                "ControlMode",StringValue (phyMode));
  
  YansWifiPhyHelper wifiPhy =  YansWifiPhyHelper::Default ();
  wifiPhy.Set("TxPowerStart",DoubleValue(10));
  wifiPhy.Set("TxPowerEnd",DoubleValue(10));
  wifiPhy.SetPcapDataLinkType (WifiPhyHelper::DLT_IEEE802_11_RADIO);

  YansWifiChannelHelper wifiChannel;
  wifiChannel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
  wifiChannel.AddPropagationLoss ("ns3::FriisPropagationLossModel");
  wifiPhy.SetChannel (wifiChannel.Create ());

  WifiMacHelper wifiMac;
  wifiMac.SetType ("ns3::AdhocWifiMac");

  NetDeviceContainer devices = wifi.Install (wifiPhy, wifiMac, c);

  //해당 위치에서의 가상 시나리오 실행
  MobilityHelper mobility;
  Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();
  positionAlloc->Add(Vector(0.0,0.0,0.0));
  positionAlloc->Add(Vector(50.0,0.0,0.0));
  positionAlloc->Add(Vector(50.0,50.0,0.0));
  positionAlloc->Add(Vector(0.0,50.0,0.0));
  mobility.SetPositionAllocator (positionAlloc);
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (c.Get(0));
  mobility.Install (c.Get(1));
  mobility.Install (c.Get(2));
  mobility.Install (c.Get(3));

  MobilityHelper mobility2;
  mobility2.SetPositionAllocator ("ns3::RandomDiscPositionAllocator",
                                 "X", StringValue ("49.0"),
                                 "Y", StringValue ("49.0"),
                                 "Rho", StringValue ("ns3::UniformRandomVariable[Min=0|Max=30]"));
  mobility2.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                             "Mode", StringValue ("Time"),
                             "Time", StringValue ("1s"),
                             "Speed", StringValue ("ns3::ConstantRandomVariable[Constant=1.0]"),
                             "Bounds", StringValue ("0|100|0|100"));
  mobility2.Install(c.Get(4));

  Config::Connect("/NodeList/*/$ns3::MobilityModel/CourseChange",MakeCallback(&CourseChange));


  InternetStackHelper internet;
  internet.Install (c);

  Ipv4AddressHelper ipv4;
  NS_LOG_INFO ("Assign IP Addresses.");
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer i = ipv4.Assign (devices);

  TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
  Ptr<Socket> recvSink = Socket::CreateSocket (c.Get (0), tid);
  InetSocketAddress local = InetSocketAddress (Ipv4Address::GetAny (), 80);
  recvSink->Bind (local);

  Ptr<Socket> source = Socket::CreateSocket (c.Get (4), tid);
  InetSocketAddress remote = InetSocketAddress (Ipv4Address ("255.255.255.255"), 80);
  source->SetAllowBroadcast (true);
  source->Connect (remote);

  Ptr<Socket> source2 = Socket::CreateSocket (c.Get (2), tid);
  InetSocketAddress remote2 = InetSocketAddress (Ipv4Address ("255.255.255.255"), 80);
  source2->SetAllowBroadcast (true);
  source2->Connect (remote2);
 
  Ptr<Socket> source3 = Socket::CreateSocket (c.Get (1), tid);
  InetSocketAddress remote3 = InetSocketAddress (Ipv4Address ("255.255.255.255"), 80);
  source3->SetAllowBroadcast (true);
  source3->Connect (remote3);

  Ptr<Socket> source4 = Socket::CreateSocket (c.Get (3), tid);
  InetSocketAddress remote4 = InetSocketAddress (Ipv4Address ("255.255.255.255"), 80);
  source4->SetAllowBroadcast (true);
  source4->Connect (remote4);

  Simulator::ScheduleWithContext (source->GetNode ()->GetId (),
                                  Seconds (1.0), &GenerateTraffic,
                                  source, packetSize, numPackets, interPacketInterval);

 //config:: tx
  Config::ConnectWithoutContext("/NodeList/*/DeviceList/*/Phy/MonitorSnifferTx",MakeCallback(&txTrace));

  //config::monitorsnifferRx -> rx,rss 
  Config::ConnectWithoutContext("/NodeList/*/DeviceList/*/Phy/MonitorSnifferRx",MakeCallback(&rxTrace));

Simulator::Stop(Seconds(20.0));
  Simulator::Run ();
  Simulator::Destroy ();

  return 0;
}
