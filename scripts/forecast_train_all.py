import pandas as pd
import json
import sagemaker
import boto3

DEBUG = True
df = pd.read_csv('train.csv')

if DEBUG: 
    print(df.head())
train_columns = list(df.columns[1:])

if DEBUG: 
    target = df['ACME']
    target.shape

    def get_split(df, freq='D', split_type = 'train', cols_to_use = ['ACME']):
    rt_set = []
    
    # use 70% for training
    if split_type == 'train':
        lower_bound = 0
        upper_bound = round(df.shape[0] * .7)
        
    # use 15% for validation
    elif split_type == 'validation':
        lower_bound = round(df.shape[0] * .7)
        upper_bound = round(df.shape[0] * .85)
        
    # use 15% for test
    elif split_type == 'test':
        lower_bound = round(df.shape[0] * .85)
        upper_bound = df.shape[0]
            
    # loop through columns you want to use
    for h in list(df):
        if h in cols_to_use:
            
            target_column = df[h].values.tolist()[lower_bound:upper_bound]
            
            date_str = str(df.iloc[0]['Date'])
            
            year = date_str[0:4]
            month = date_str[4:6]
            date = date_str[7:]
                                                
            start_dataset = pd.Timestamp("{}-{}-{} 00:00:00".format(year, month, date, freq=freq))
                        
            # create a new json object for each column
            json_obj = {'start': str(start_dataset),
                       'target':target_column}
    
            rt_set.append(json_obj)
    
    return rt_set

train_set = get_split(df)
test_set = get_split(df, split_type = 'test')

def write_dicts_to_file(path, data):
    with open(path, 'wb') as fp:
        for d in data:
            fp.write(json.dumps(d).encode("utf-8"))
#             fp.write("\n".encode('utf-8'))

write_dicts_to_file('train.json', train_set)
write_dicts_to_file('test.json', test_set)

if IPYNB: 
    !aws s3 cp train.json s3://forecasting-do-not-delete/train/train.json
    !aws s3 cp test.json s3://forecasting-do-not-delete/test/test.json
    sess = sagemaker.Session()
    region = sess.boto_region_name
    image = sagemaker.amazon.amazon_estimator.get_image_uri(region, "forecasting-deepar", "latest")
    role = sagemaker.get_execution_role()   
    estimator = sagemaker.estimator.Estimator(
        sagemaker_session=sess,
        image_name=image,
        role=role,
        train_instance_count=1,
        train_instance_type='ml.c4.2xlarge',
        base_job_name='deepar-electricity-demo',
        output_path='s3://forecasting-do-not-delete/output'
    )

    hyperparameters = {
    
    # frequency interval is once per day
        "time_freq": 'D',
        "epochs": "400",
        "early_stopping_patience": "40",
        "mini_batch_size": "64",
        "learning_rate": "5E-4",
        
        # let's use the last 30 days for context
        "context_length": str(30),
        
        # let's forecast for 30 days
        "prediction_length": str(30)
    }

    estimator.set_hyperparameters(**hyperparameters)
    data_channels = {
        "train": "s3://forecasting-do-not-delete/train/train.json",
        "test": "s3://forecasting-do-not-delete/test/test.json"
    }

    estimator.fit(inputs=data_channels, wait=True)