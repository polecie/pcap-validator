from pickle import TRUE
from nfstream import NFStreamer, NFPlugin
import pandas as pd
class Packet40Count(NFPlugin):
    def on_init(self, pkt, flow):
        if pkt.ip_size == 40:
            flow.udps.packet_with_40_ip_size=1
        else:
            flow.udps.packet_with_40_ip_size=0
        
    def on_update(self, pkt, flow):
        if pkt.ip_size == 40:
            flow.udps.packet_with_40_ip_size += 1

col_list = ['src_ip','dst_ip','bidirectional_packets','bidirectional_bytes','application_name','application_category_name']

def summary_data(file_name):
    streamer = NFStreamer(file_name).to_pandas()
    if 'VPN' in streamer['application_category_name'].unique() or 'IPsec' in str(streamer['application_name'].unique()):
        app_bytes = (streamer.groupby(['application_name','application_category_name'],as_index=False)['bidirectional_bytes'].sum())
        streamer_info = streamer[col_list].drop_duplicates(['src_ip', 'dst_ip', 'application_name'])
        return app_bytes, streamer_info
    return "there's no information about VPN or everything just got simply crashed :)"
        
if __name__ == "__main__":
    print(summary_data('files\ipsec.pcap'))