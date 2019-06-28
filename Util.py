import os
import time

path_spiter = '/'

def save_data_batch(gid, data_arr, root_path):
    if (data_arr.__len__() > 0):
        date_str = time.strftime('%Y%m%d', data_arr[0][0])

        if (os.path.exists(root_path)):
            sub_dir = root_path + path_spiter + date_str
            if not (os.path.exists(sub_dir)):
                os.mkdir(sub_dir)
            file_path = sub_dir + path_spiter + gid + ".txt"
            if not (os.path.isfile(file_path)):
                fp = open(file_path, mode='w')
                fp.writelines(date_str + '\r\n')
                fp.close()
            fp = open(file_path, mode='r')
            lines = fp.readlines()
            fp.close()
            for data in data_arr:
                time_str = time.strftime('%H:%M:%S', data[0])
                is_duplicate = False
                line_str = time_str + '\t' + str(data[1]).strip() + '\t' + str(data[2]).strip() + '\t' + data[3].strip()
                for line in lines:
                    if line.strip() == line_str:
                        is_duplicate = True
                        break
                if is_duplicate == False:
                    fp = open(file_path, mode='a')
                    fp.write(line_str + '\r\n')
                    fp.close()



def save_data(gid, date_time, price, volume, direction_type, root_path):
    date_str = time.strftime('%Y%m%d', date_time)
    time_str = time.strftime('%H:%M:%S', date_time)
    if (os.path.exists(root_path)):
        sub_dir = root_path + path_spiter + date_str
        if not(os.path.exists(sub_dir)):
            os.mkdir(sub_dir)
        file_path = sub_dir + path_spiter + gid + ".txt"
        if not(os.path.isfile(file_path)):
            fp = open(file_path, mode='w')
            fp.writelines(date_str+'\r\n')
            fp.close()
        fp = open(file_path, mode='r')
        lines = fp.readlines()
        fp.close()
        is_duplicate = False
        for line in lines:
            if line.strip() == time_str + '\t' + str(price).strip() + '\t' + str(volume).strip() + '\t' + direction_type.strip():
                is_duplicate = True
                break
        if not(is_duplicate):
            fp = open(file_path, mode='a')
            fp.write(time_str + '\t' + str(price) + '\t' + str(volume) + '\t' + direction_type + '\r\n')
            fp.close()

#print(time.strftime('%H:%M:%S', time.localtime()))

#save_data('sh600031', time.strptime('2019-6-21 9:30:20', '%Y-%m-%d %H:%M:%S'), 12.31, 10300, os.getcwd() + '/data')

#save_data('sh600031', time.strptime('2019-6-21 9:31:55', '%Y-%m-%d %H:%M:%S'), 12.32, 11000, os.getcwd() + '/data')