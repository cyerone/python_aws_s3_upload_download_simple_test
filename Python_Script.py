import boto3
import time
import os
import sys 

s3=boto3.resource('s3')
results_list = []

def main():
    encrypted_bucket_name = sys.argv[1]
    unencrypted_bucket_name = sys.argv[2]
    results_bucket_name = sys.argv[3]

    create_test_file("10mb_testfile",10)
    create_test_file("100mb_testfile",100)
    create_test_file("1gb_testfile",1000)

    test_upload(50, encrypted_bucket_name, "10mb_testfile", "ue10_result.txt")
    test_upload(50, unencrypted_bucket_name, "10mb_testfile", "uu10_result.txt")
    test_download(50, encrypted_bucket_name, "10mb_testfile", "de10_result.txt")
    test_download(50, unencrypted_bucket_name, "10mb_testfile", "du10_result.txt")

    test_upload(50, encrypted_bucket_name, "100mb_testfile", "ue100_result.txt")
    test_upload(50, unencrypted_bucket_name, "100mb_testfile", "uu100_result.txt")
    test_download(50, encrypted_bucket_name, "100mb_testfile", "de100_result.txt")
    test_download(50, unencrypted_bucket_name, "100mb_testfile", "du100_result.txt")

    test_upload(50, encrypted_bucket_name, "1000mb_testfile", "ue1000_result.txt")
    test_upload(50, unencrypted_bucket_name, "1000mb_testfile", "uu1000_result.txt")
    test_download(50, encrypted_bucket_name, "1000mb_testfile", "de1000_result.txt")
    test_download(50, unencrypted_bucket_name, "1000mb_testfile", "du1000_result.txt")

    upload_results(results_list, results_bucket_name)

    

def upload_to_bucket(file, bucket):
    s3.meta.client.upload_file(file,bucket,file)

def download_from_bucket(file,bucket):
    s3.Bucket(bucket).download_file(file,file)

def test_upload(count, bucket, file, output):
    output_file = open(output, "w")
    for x in range(count):
        start_time = time.time()
        upload_to_bucket(file,bucket)
        stop_time = time.time()
        measured_time = str(stop_time-start_time)
        output_file.write(measured_time)
        output_file.write("\n")
        print(x+1, ": ", measured_time)
    output_file.close()
    results_list.append(output)

def test_download(count, bucket, file, output):
    output_file = open(output, "w")
    for x in range(count):
        start_time = time.time()
        download_from_bucket(file,bucket)
        stop_time = time.time()
        measured_time = str(stop_time-start_time)
        output_file.write(measured_time)
        output_file.write("\n")
        print(x+1, ": ", measured_time)
    output_file.close()
    results_list.append(output)

def upload_results(results_list, results_bucket):
    for results in results_list:
        upload_to_bucket(results, results_bucket)

def create_test_file(name, size_in_MB):
    test_file = open(name, "wb")
    test_file.write(os.urandom(size_in_MB*1048576))
    test_file.close
    print("file: \"", name, "\" (", size_in_MB, "MB ) was created.")







