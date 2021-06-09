function bw_cost = data_serv_delivery_opt_bwcost(N,M,beta,bw_edge,mem_edge,mem_occup,mem_app,serv_send_data,serv_recv_data,serv_capa,serv_occup,serv_app,exec_time,x,v2e_trvtime,vel_free,bandwidth,density_jam,density,bw_const,l_cov)

nov = N;
noe = M;

cvx_begin
    variable mem(nov,noe);
    variable serv(nov,noe) binary;

    expression serv_mem_int(noe);
    expression mem_int(noe);
    expression bytes_received_min(nov,noe);
    expression serv_bytes_received_min(nov,noe);
    expression data_bw_util(noe);
    expression serv_bw_util(noe);
    expression bw_util(noe);
    expression bw_cost;
    expression serv_accum_vehicle(nov);
    expression serv_mem_accum_edge(noe);
    expression serv_capa_accum_edge(noe);
    expression mem_accum_vehicle(nov);
    expression mem_accum_edge(noe);
    
    for j = 1:noe
        for i = 1:nov
            mem_int(j) = mem_int(j) + mem(i,j);
            serv_mem_int(j) = serv_mem_int(j) + serv(i,j)*(serv_send_data(i)+serv_recv_data(i));
            bytes_received_min(i,j) = x(i,j) * bandwidth(j)/(density_jam(j)*(vel_free(j)/3600)*(1-(density(j)/density_jam(j))));
            serv_bytes_received_min(i,j) = x(i,j) * (bandwidth(j)*((l_cov(j)/((vel_free(j)/3600)*(1-(density(j)/density_jam(j)))))-exec_time(i)))/(density_jam(j)*l_cov(j));
        end
    end
    
    for j = 1:noe
        data_bw_util(j) = (((mem_int(j)*(vel_free(j)/3600)*(1-(density(j)/density_jam(j))))/l_cov(j))+bw_const(j))/bandwidth(j);    
        for i = 1:nov
            serv_bw_util(j) = serv_bw_util(j)+ (serv(i,j)*(serv_send_data(i)+serv_recv_data(i))/((l_cov(j)/((vel_free(j)/3600)*(1-(density(j)/density_jam(j)))))-exec_time(i)))/bandwidth(j);
        end
        bw_util(j) = data_bw_util(j) + serv_bw_util(j);
        bw_cost = bw_cost + beta*(1+bw_util(j))^2;
    end
    
    for i = 1:nov
        for j = 1:noe
            mem_accum_vehicle(i) = mem_accum_vehicle(i) + mem(i,j)*x(i,j);
        end
    end

    for j = 1:noe
         for i = 1:nov
             mem_accum_edge(j) = mem_accum_edge(j) + mem(i,j)*x(i,j);
         end
    end

    for i = 1:nov
        for j = 1:noe
            serv_accum_vehicle(i) = serv_accum_vehicle(i) + serv(i,j)*x(i,j);
        end
    end

    for j = 1:noe
        for i = 1:nov
            serv_mem_accum_edge(j) = serv_mem_accum_edge(j) + serv(i,j)*(serv_send_data(i)+serv_recv_data(i))*x(i,j);
        end
    end
    
    for j = 1:noe
        for i = 1:nov
            serv_capa_accum_edge(j) = serv_capa_accum_edge(j) + serv(i,j)*serv_app(i)*x(i,j);
        end
    end
    
    minimize bw_cost
    subject to
        for i = 1:nov
            mem_accum_vehicle(i) == mem_app(i);
        end
        for i = 1:nov
            for j = 1:noe
                if (x(i,j) == 1)
                    mem(i,j) >= 0;
                end
            end
        end
        for i = 1:nov
            for j = 1:noe
                if (x(i,j) == 1)
                    mem(i,j) <= mem_app(i);
                end
            end
        end
        
        for i = 1:nov
            for j = 1:noe
                if (x(i,j) == 0)
                    mem(i,j) == 0;
                end
            end
        end

        for i = 1:nov
            serv_accum_vehicle(i) == 1;
        end

        for j = 1:noe
            serv_capa_accum_edge(j) <= serv_capa(j) - serv_occup(j);
        end

        for j = 1:noe
            mem_accum_edge(j) + serv_mem_accum_edge(j) <= mem_edge(j) - mem_occup(j);
        end

        for i = 1:nov
            for j = 1:noe
                (mem(i,j)/(bw_edge)) <= v2e_trvtime(i,j)*3600;
            end
        end

        for i = 1:nov
            for j = 1:noe
                bytes_received_min(i,j) >= mem(i,j) + serv(i,j)*(serv_send_data(i)+serv_recv_data(i));
            end
        end
cvx_end