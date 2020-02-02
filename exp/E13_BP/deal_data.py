def deal_data(input_name, output_name):
    train_data = open(input_name)
    f = open(output_name, 'w+')
    data = []
    while 1:
        line_ = train_data.readline()
        if not line_:
            break
        line_ = line_[:-1]
        line_ = line_.split(' ')
        data.append(line_)
    num = len(data)
    for i in range(num):
        attr_num = len(data[i])
        no = False
        for j in range(attr_num):
            if data[i][j] == '?':
                data[i][j] = '-1'
            if j == 28:
                no = True
        if no:
            data[i] = data[i][:-1]
        print(','.join(data[i]), file=f)
    train_data.close()
    f.close()

deal_data('horse-colic.data', 'train.data')
deal_data('horse-colic.test', 'test.data')
