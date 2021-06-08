function bw_cost = serv_delivery_opt_bwcost(ov_sets,len_of_sets,N,M,beta,bw_edge,mem_edge,mem_occup,serv_send_data,serv_recv_data,serv_capa,serv_occup,serv_app,exec_time,x,v2e_trvtime,vel_free,bandwidth,density_jam,density,bw_const,l_cov)

nov = N;
noe = M;

cvx_begin
    variable serv(nov,noe) binary;
    
    expression serv_mem_int(noe);
    expression serv_bytes_received_min(nov,noe);
    expression serv_bw_util(noe);
    expression bw_cost;
    expression serv_accum_vehicle(nov);
    expression serv_mem_accum_edge(noe);
    expression serv_capa_accum_edge(noe);
    expression temp_sum(len_of_sets(noe+1));
    expression serv_temp_sum(len_of_sets(noe+1));
    
    for j = 1:noe
        for i = 1:nov
            serv_mem_int(j) = serv_mem_int(j) + serv(i,j)*(serv_send_data(i)+serv_recv_data(i));
            serv_bytes_received_min(i,j) = x(i,j) * (bandwidth(j)*((l_cov(j)/((vel_free(j)/3600)*(1-(density(j)/density_jam(j)))))-exec_time(i)))/(density_jam(j)*l_cov(j));
        end
    end
    
    for j = 1:noe
        for i = 1:nov
            serv_bw_util(j) = serv_bw_util(j)+ (serv(i,j)*(serv_send_data(i)+serv_recv_data(i))/((l_cov(j)/((vel_free(j)/3600)*(1-(density(j)/density_jam(j)))))-exec_time(i))/bandwidth(j);
        end
        bw_cost = bw_cost + beta * (1+serv_bw_util(j))^2;
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

%     for j = 1:noe
%         for k = len_of_sets(j)+1:len_of_sets(j+1)
%             for i = 1:nov
%                 temp_sum(k) = temp_sum(k) + serv(i,j)*(serv_send_data(i)+serv_recv_data(i))*ov_sets(k,i);
%             end
%         end
%     end
% 
%     for j = 1:noe
%         for k = len_of_sets(j)+1:len_of_sets(j+1)
%             for i = 1:nov
%                 serv_temp_sum(k) = serv_temp_sum(k) + serv(i,j)*serv_app(i)*ov_sets(k,i);
%             end
%         end
%     end
    
    minimize bw_cost
    subject to
        for i = 1:nov
            serv_accum_vehicle(i) == 1;
        end
      
        for j = 1:noe
            serv_mem_accum_edge(j) <= mem_edge(j) - mem_occup(j);
        end
        for j = 1:noe
            serv_capa_accum_edge(j) <= serv_capa(j) - serv_occup(j);
        end
        
%         for j = 1:noe
%             for k = len_of_sets(j)+1:len_of_sets(j+1)
%                 temp_sum(k) <= mem_edge(j) - mem_occup(j);
%             end        
%         end
% 
%         for j = 1:noe
%             for k = len_of_sets(j)+1:len_of_sets(j+1)
%                 serv_temp_sum(k) <= serv_capa(j) - serv_occup(j);
%             end                
%         end

        for i = 1:nov
            for j = 1:noe
                serv_bytes_received_min(i,j) >= serv(i,j)*(serv_send_data(i)+serv_recv_data(i));
            end
        end
cvx_end