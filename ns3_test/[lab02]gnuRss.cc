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
 * Author: Guangyu Pei <guangyu.pei@boeing.com>
 */

//written by 김진아, 2020
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-phy.h"
#include "ns3/gnuplot.h"
#include "ns3/command-line.h"
#include "ns3/config.h"
#include "ns3/double.h"
#include "ns3/string.h"
#include "ns3/log.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/yans-wifi-channel.h"
#include "ns3/mobility-model.h"
#include "ns3/internet-stack-helper.h"
#include "ns3/ipv4-address-helper.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("ClearChannelCmu");

static double rss;

//get rss
void PhyTrace(Ptr<const Packet> packet,uint16_t channelFreqMhz,WifiTxVector txVector,MpduInfo aMpdu,SignalNoiseDbm signalNoise){
	rss=signalNoise.signal;
}

Ptr<Socket> SetupPacketReceive (Ptr<Node> node)
{
  TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
  Ptr<Socket> sink = Socket::CreateSocket (node, tid);
  InetSocketAddress local = InetSocketAddress (Ipv4Address::GetAny (), 80);
  sink->Bind (local);
 
  return sink;
}

void GenerateTraffic (Ptr<Socket> socket, uint32_t pktSize,
                             uint32_t pktCount, Time pktInterval )
{
  if (pktCount > 0)
    {
      socket->Send (Create<Packet> (pktSize));
      Simulator::Schedule (pktInterval, &GenerateTraffic,
                           socket, pktSize,pktCount - 1, pktInterval);
    }
  else
    {
      socket->Close ();
    }
}

//by 김진아, 가상 네트워크환경 실행 함수
double Run (double distance,const WifiHelper &wifi, const YansWifiPhyHelper &wifiPhy,const WifiMacHelper &wifiMac, const YansWifiChannelHelper &wifiChannel)
{
  
  NodeContainer c;
  c.Create (2);

  InternetStackHelper internet;
  internet.Install (c);

  YansWifiPhyHelper phy = wifiPhy;
  phy.SetChannel (wifiChannel.Create ());

  WifiMacHelper mac = wifiMac;
  NetDeviceContainer devices = wifi.Install (phy, mac, c);

  MobilityHelper mobility;
  Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();
  positionAlloc->Add (Vector (0.0, 0.0, 0.0));
  positionAlloc->Add (Vector (distance, 0.0, 0.0));
  mobility.SetPositionAllocator (positionAlloc);
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (c);

  Ipv4AddressHelper ipv4;
  NS_LOG_INFO ("Assign IP Addresses.");
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer i = ipv4.Assign (devices);

  Ptr<Socket> recvSink = SetupPacketReceive (c.Get (0));

  TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
  Ptr<Socket> source = Socket::CreateSocket (c.Get (1), tid);
  InetSocketAddress remote = InetSocketAddress (Ipv4Address ("255.255.255.255"), 80);
  source->SetAllowBroadcast (true);
  source->Connect (remote);

  uint32_t packetSize = 1000;
  uint32_t maxPacketCount = 200;

  Time interPacketInterval = Seconds (1.);
  
  Simulator::Schedule (Seconds (1.0), &GenerateTraffic, source, packetSize, maxPacketCount,interPacketInterval);
  
  Config::ConnectWithoutContext("/NodeList/0/DeviceList/*/Phy/MonitorSnifferRx",MakeCallback(&PhyTrace));

  Simulator::Run ();

  Simulator::Destroy ();
  return rss;
}

int main (int argc, char *argv[])
{

	  CommandLine cmd;
	  cmd.Parse(argc,argv);

	  //by 김진아, 거리에 따른 rss 그래프 생성
	  Gnuplot gnuplot1=Gnuplot("rssDistance(dbm).pdf");
	  gnuplot1.SetTitle("rssDistance(Dbm)");
	  gnuplot1.SetLegend("distance","rss");

	  Gnuplot gnuplot2=Gnuplot("rssDistance(watt).pdf");
	  gnuplot2.SetTitle("rssDistance(Watt)");
	  gnuplot2.SetLegend("distance","rss");
	
	  Gnuplot2dDataset dataset1;
	  dataset1.SetTitle("rss");
	  dataset1.SetStyle(Gnuplot2dDataset::LINES_POINTS);

	  Gnuplot2dDataset dataset2;
	  dataset2.SetTitle("rss");
	  dataset2.SetStyle(Gnuplot2dDataset::LINES_POINTS);


	//by 김진아, 데이터 수집 및 저장 
	for(double distance=0.0; distance<100; distance+=1){
	
		  std::string phyMode("DsssRate1Mbps");

		  //wifi 환경 구축
          WifiHelper wifi;
          wifi.SetStandard (WIFI_PHY_STANDARD_80211b);
          WifiMacHelper wifiMac;
          Config::SetDefault ("ns3::WifiRemoteStationManager::NonUnicastMode", StringValue (phyMode));
          wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
                                        "DataMode",StringValue (phyMode),
                                        "ControlMode",StringValue(phyMode));
          wifiMac.SetType ("ns3::AdhocWifiMac");

          YansWifiPhyHelper wifiPhy = YansWifiPhyHelper::Default ();
          wifiPhy.Set("TxPowerStart",DoubleValue(10));
          wifiPhy.Set("TxPowerEnd",DoubleValue(10));
  
          YansWifiChannelHelper wifiChannel;
          wifiChannel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
          wifiChannel.AddPropagationLoss ("ns3::FriisPropagationLossModel");

          wifiPhy.SetChannel(wifiChannel.Create());

          double pktsRecvd =Run (distance,wifi,wifiPhy,wifiMac,wifiChannel);

		  //데이터 저장
		  dataset1.Add (distance,pktsRecvd);
          dataset2.Add(distance,DbmToW(pktsRecvd));
	}

  //by 김진아, 데이터들 그리기
  gnuplot1.AddDataset (dataset1);  
  gnuplot2.AddDataset (dataset2);
  std::ofstream plotfile("rssDistance1.txt");
  std::ofstream plotfile2("rssDistance2.plt");
  gnuplot1.GenerateOutput (plotfile);
  gnuplot2.GenerateOutput(plotfile2);
  plotfile.close ();
  plotfile2.close();

  return 0;
}
