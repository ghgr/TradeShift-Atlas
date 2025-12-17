import json
import pandas as pd

def parse_file():

    with open("data/TradeData.json") as f:
        raw = json.load(f)


    money = {}

    period0 = 0
    for elem in raw:
        # skip aggregates like World
        if elem['reporterISO'] == "W00" or elem['partnerISO'] == "W00":
            continue

        # money flow: FROM (payer) -> TO (payee), reported by FROM
        # only importer-reported payments
        if elem['flowDesc'] != "Import":
            continue

        payer  = elem['reporterISO']   # importer
        payee  = elem['partnerISO']    # exporter / counterparty
        period = elem['refPeriodId']
        value  = elem['primaryValue']   # CIF, USD

        k = (payer, payee, period)

        if period!=period0:
            print(period)
            period0 = period

        money[k] = value

    print(len(raw))

    return money


def get_flows(money, period):
    countries = list(set([v[0] for v in money.keys()]))
    flows = {}
    for i0 in range(0,len(countries)):
        for i1 in range(i0, len(countries)):
            if i0==i1: continue
            c0 = countries[i0]
            c1 = countries[i1]
            value = money.get((c0,c1,period),0) + money.get((c1,c0,period), 0)
            flows[(c0,c1)] = value
    
    return flows



def get_edge(flows, c0, c1):
    if (c0,c1) in flows:
        return flows[(c0,c1)]
    return flows[(c1,c0)]


def get_all_edges_from_country(flows, c0):
    res = {}
    countries = sorted(list(set([v[0] for v in flows.keys()])))
    s=0
    for c1 in countries:
        if c0==c1: continue
        s+=get_edge(flows, c0, c1)

    for c1 in countries:
        if c0==c1: continue
        res[c1] =  get_edge(flows, c0, c1)/s

    return res


def get_all_edges(money, period):
    flows = get_flows(money, period)

    edges = {}
    countries = sorted(list(set([v[0] for v in flows.keys()])))
    for c0 in countries:
        edges[c0] = get_all_edges_from_country(flows, c0)

    return pd.DataFrame(edges).sort_index()
    

if __name__=="__main__":

    money = parse_file()
    df0 = get_all_edges(money, 20150101)
    df1 = get_all_edges(money, 20240101)

    df = df1-df0



