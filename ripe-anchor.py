import json
from datetime import datetime
from ripe.atlas.sagan import (
    PingResult,
    Result,
    SslResult
)
import requests
import csv
import time
from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest,
  AtlasResultsRequest
)


def get_API_key() -> str:
    """ Return RIPE API KEY by reading it from a file.
    A file, api_key, is required and the file should contain
    the API key in the first line.
    :return key: (str): API key
    """
    with open("api_key", "r") as f:
        key = f.readline()
    return key

def set_ping(target: str, desc: str) -> Ping:
    """Set parameter for ping.
    :param target: (str) ping target, either an url or ip
    :param desc: (str) description of the experiments
    :return ping: (Ping) Ping object
    """
    ping = Ping(af=4, target=target, description=desc)
    return ping

def set_traceroute(target: str, desc: str) -> Traceroute:
    """Set parameter for traceroute
    :param target: (str) ping target, either an url or ip
    :param desc: (str) description of the experiments
    :return traceroute: (Traceroute) Traceroute object
    """
    traceroute = Traceroute(
        af=4,
        target=target,
        description=desc,
        protocol="ICMP",
    )
    return traceroute


def set_src() -> AtlasSource:
    """TODO: the function needs to be updated.
    """
    with open('anchorSelection.csv', 'r') as csvinput:
        reader = csv.reader(csvinput)
        header = next(reader)
        probe_id = ""
        i = 0
        for rows in reader:
            probe_id += str(rows[2]) + ","
            i += 1
        probe_id = probe_id[:-1]  # to run all use probe_id[:-1]
        # print(probe_id)
        # print(i)

    source = AtlasSource(
                type="probes",
                value=probe_id,
                requested=i,
                tags={"include": ["system-ipv4-works"]},
                action="add"
            )

    return source
    # source = AtlasSource(
    #     type="probes",
    #     value="6771",
    #     requested=1,
    #     tags={"include":["system-ipv4-works"]}
    # )

    # source1 = AtlasSource(
    #     type="country",
    #     value="NL",
    #     requested=50,
    #     tags={"exclude": ["system-anchor"]}
    # )
    # return source

def run_exp(api_key: str, meas: list, srcs: list) -> (bool, str):
    """ Run Atlas experiments
    :param api_key: (str): API key
    :param meas: (list): list of experiments to run
    :param srcs: (list): list of sources
    :return is_success: (bool): True if the experiment was successful
    :return response: (str): the measurement ID
    """
    atlas_request = AtlasCreateRequest(
        start_time=datetime.utcnow(),
        key=api_key,
        measurements=meas,
        sources=srcs,
        is_oneoff=True
    )
    (is_success, response) = atlas_request.create()
    return (is_success, response)


def get_results(meas_id: str) -> (bool, list):
    """ Get results.
    :param meas_id: (str): measurement id to retrieve its results
    :return is_success: (bool):  True if the experiment was successful
    :return results: (list): results of the measurement
    """
    kwargs = {
        "msm_id": meas_id
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()

    return (is_success, results)


def main():
    atlas_api_key = get_API_key()

    ### setting
    description = "testing new wrapper"
    f = open('vpn_configs.csv', 'r')
    file = csv.DictReader(f)
    target_list = []
    measurement_id_list_ping = {}
    #measurement_id_list_tr = {}
    #store all of the IP addresses of the targeted VPN servers
    for col in file:
        target_list.append(col['ip'])
    target_list1 = target_list[:70]
    target_list_2 = target_list[70:140]
    target_list_3 = target_list[140:210]
    target_list_4 = target_list[210:280]
    target_list_5 = target_list[280:350]
    target_list_6 = target_list[350:420]
    target_list_7 = target_list[420:490]
    target_list_8 = target_list[490:540]
    target_list_9 = target_list[540:]
    #for every target in the target list
    for target in target_list_7:

        ping_obj = set_ping(target, description)
        # trace_obj = set_traceroute(target, description)
        source = set_src()

        time.sleep(20)
        is_exp_success_ping, response = run_exp(atlas_api_key, [ping_obj], [source])
        #is_exp_success_traceroute, response_tr = run_exp(atlas_api_key, [trace_obj], [source])


        print(is_exp_success_ping, response, target)
        if is_exp_success_ping:
            id_ping = response['measurements']
            measurement_id_list_ping[str(target)] = str(id_ping)



    with open('measurement_id_ping.csv', 'a') as csvoutput: #replace w with a for other files
        writer = csv.writer(csvoutput)
        # writer = csv.writer(csvoutput, lineterminator='\n') #fieldnames = ["measurement id"] writer = csv.writer(csvoutput, fieldnames=fieldnames)
        # writer.writerow(["IP","measurement id"])
        for key in measurement_id_list_ping.keys():
            msm = measurement_id_list_ping[key].replace("[","").replace("]","")
            writer.writerow([key] + [msm])



    # print(is_exp_success_traceroute, response_tr, target)
    # if is_exp_success_traceroute:
    #     id_tr = response_tr['measurements']
    #     measurement_id_list_tr.append(id_tr)
    #
    # with open('measurement_id_traceroute.csv', 'w') as csvoutput:
    #     writer = csv.writer(csvoutput, lineterminator='\n')
    #     writer.writerow("measurement id")
    #     for measurement_id in measurement_id_list_tr:
    #         writer.writerow(measurement_id)




    # target = "www.google.com"
    # ping_obj = set_ping(target, description)
    # trace_obj = set_traceroute(target, description)
    # source = set_src()

    ### run exp
    # is_exp_success, response = run_exp(atlas_api_key, [ping_obj], [source])
    # is_exp_success_traceroute, response = run_exp(atlas_api_key, [trace_obj], [source])
    # print(is_exp_success_traceroute, response)

    # sleep

    ## get results
    if is_exp_success_ping:
        is_result_success, results = get_results(response)
        if is_result_success:
            print("results: "+results)







if __name__ == "__main__":
    main()


# import json
# from datetime import datetime
# from ripe.atlas.sagan import (
#     PingResult,
#     Result,
#     SslResult
# )
# import requests
# import csv
# import time
# from ripe.atlas.cousteau import (
#   Ping,
#   Traceroute,
#   AtlasSource,
#   AtlasCreateRequest,
#   AtlasResultsRequest
# )
# import json
# from urllib.request import urlopen
# import ssl
#
#
#
# def get_API_key() -> str:
#     """ Return RIPE API KEY by reading it from a file.
#     A file, api_key, is required and the file should contain
#     the API key in the first line.
#     :return key: (str): API key
#     """
#     with open("api_key", "r") as f:
#         key = f.readline()
#     return key
#
# def set_ping(target: str, desc: str) -> Ping:
#     """Set parameter for ping.
#     :param target: (str) ping target, either an url or ip
#     :param desc: (str) description of the experiments
#     :return ping: (Ping) Ping object
#     """
#     ping = Ping(af=4, target=target, description=desc)
#     return ping
#
# def set_traceroute(target: str, desc: str) -> Traceroute:
#     """Set parameter for traceroute
#     :param target: (str) ping target, either an url or ip
#     :param desc: (str) description of the experiments
#     :return traceroute: (Traceroute) Traceroute object
#     """
#     traceroute = Traceroute(
#         af=4,
#         target=target,
#         description=desc,
#         protocol="ICMP",
#     )
#     return traceroute
#
# def set_src() -> AtlasSource:
#     """TODO: the function needs to be updated.
#     """
#     with open('anchorSelection.csv', 'r') as csvinput:
#         reader = csv.reader(csvinput)
#         header = next(reader)
#         probe_id = ""
#         i = 0
#         for rows in reader:
#             probe_id += str(rows[2]) + ","
#             i += 1
#         probe_id = probe_id[:14]  # to run all use probe_id[:-1]
#         print(probe_id)
#         print(i)
#
#         source = AtlasSource(
#             type="probes",
#             value=probe_id,
#             requested=3,
#             tags={"include": ["system-ipv4-works"]},
#             action="add"
#         )
#
#         return source
#     # source = AtlasSource(
#     #     type="probes",
#     #     value="6771",
#     #     requested=1,
#     #     tags={"include":["system-ipv4-works"]}
#     # )
#
#     # source1 = AtlasSource(
#     #     type="country",
#     #     value="NL",
#     #     requested=50,
#     #     tags={"exclude": ["system-anchor"]}
#     # )
#     # return source
#
# def run_exp(api_key: str, meas: list, srcs: list) -> (bool, str):
#     """ Run Atlas experiments
#     :param api_key: (str): API key
#     :param meas: (list): list of experiments to run
#     :param srcs: (list): list of sources
#     :return is_success: (bool): True if the experiment was successful
#     :return response: (str): the measurement ID
#     """
#     atlas_request = AtlasCreateRequest(
#         start_time=datetime.utcnow(),
#         key=api_key,
#         measurements=meas,
#         sources=srcs,
#         is_oneoff=True
#     )
#     (is_success, response) = atlas_request.create()
#     return (is_success, response)
#
#
# def get_results(meas_id: str) -> (bool, list):
#     """ Get results.
#     :param meas_id: (str): measurement id to retrieve its results
#     :return is_success: (bool):  True if the experiment was successful
#     :return results: (list): results of the measurement
#     """
#     kwargs = {
#         "msm_id": meas_id
#     }
#     is_success, results = AtlasResultsRequest(**kwargs).create()
#
#     return (is_success, results)
#
#
# def main():
#     atlas_api_key = get_API_key()
#
#     ### setting
#     description = "testing new wrapper"
#     target = "www.google.com"
#     ping_obj = set_ping(target, description)
#     trace_obj = set_traceroute(target, description)
#     source = set_src()
#
#     ### run exp
#     is_exp_success, response = run_exp(atlas_api_key, [ping_obj], [source])
#     print("response", is_exp_success, response)
#     # sleep
#
#     ## get results
#     if is_exp_success:
#         is_result_success, results = get_results(response)
#         if is_result_success:
#             print(results)
#     time.sleep(5)
#
#     update_file(str(response["measurements"][0]))
#
#
#
#
#     #code for traceroute works
#     is_exp_success_trace, response_trace = run_exp(atlas_api_key, [trace_obj], [source])
#     print(is_exp_success_trace, response_trace)
#     #update_file(str(response["measurements"][0]))
#     # sleep
#
#     ## get results
#     if is_exp_success_trace:
#         is_result_success_trace, results_trace = get_results(response_trace)
#         if is_result_success_trace:
#             print(results_trace)
#
#     time.sleep(5)
#     store_traceroute(str(response_trace["measurements"][0]))
#
# def update_file(measurement_id: str):
#     #measurement_id="46400779"
#
#     print("Measurement ID", measurement_id)
#     ssl._create_default_https_context = ssl._create_unverified_context
#     URL = 'https://atlas.ripe.net//api/v2/measurements/' + measurement_id + '/results/?format=json'
#     data = json.loads(urlopen(URL).read())
#     print("data",data)
#     print("data Len",len(data))
#
#     with open('anchorSelectionAll.csv','r') as csvinput:
#         with open('AnchorSelectionAllInfoWithRTT.csv', 'w') as csvoutput:
#             writer = csv.writer(csvoutput, lineterminator='\n')
#             reader = csv.reader(csvinput)
#             all = []
#             header = next(reader)
#             writer.writerow(header + ["RTT"])
#             ping_data = {}
#             for i in range(len(data)):
#                 if data[i]['result'][1].get('rtt') != None:
#                     rtt = data[i]['result'][1]['rtt']
#                     print("rtt", rtt)
#                 else:
#                     rtt = "None"
#                 ping_data[data[i]['prb_id']] = rtt
#
#             print(ping_data)
#             for row in reader:
#                 p_id = row[2]
#
#                 #print(ping_data[int(p_id)])
#                 if ping_data.__contains__(int(p_id)):
#                     row.append(ping_data[int(p_id)])
#                     all.append(row)
#
#                 #print(row)
#
#
#             writer.writerows(all)
#
# def store_traceroute(measurement_id: str):
#
#     ssl._create_default_https_context = ssl._create_unverified_context
#     URL = 'https://atlas.ripe.net//api/v2/measurements/' + measurement_id + '/results/?format=json'
#     data = json.loads(urlopen(URL).read())
#
#     list = []
#
#     for i in range(len(data)):
#         if data[i]['result'] != None:
#             list.append({data[i]['prb_id']: data[i]['result']})
#      # list.append(dictionary)
#
#     json_object = json.dumps(list, indent=5)
#     with open("traceroute.json", "w") as outfile:
#         outfile.write(json_object)
#
#
# if __name__ == "__main__":
#     main()
