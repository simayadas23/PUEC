def relax(u,v,wObj,wt_u_v):
    #print ("u, v, d_v[v], d_v[u], wt_u_v", u, v, wObj.d_v[v], wObj.d_v[u], wt_u_v)
    if (wObj.d_v[v] > (wObj.d_v[u] + wt_u_v)) and (wt_u_v !=0 ):        
        wObj.d_v[v] = (wObj.d_v[u] + wt_u_v)
        wObj.pi_v[v] = u