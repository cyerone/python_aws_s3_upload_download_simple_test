import boto3
import time
import os
import sys 

s3=boto3.resource('s3')

def main():
    results_list = []
    encrypted_sse_kms_bucket_name = sys.argv[1]
    encrypted_sse_s3_bucket_name = sys.argv[2]
    unencrypted_bucket_name = sys.argv[3]
    results_bucket_name = sys.argv[4]

    create_test_file("10mb_testfile",10)
    test_upload(100, encrypted_sse_kms_bucket_name, "10mb_testfile", "uek10_result.txt", results_list)
    test_upload(100, encrypted_sse_s3_bucket_name, "10mb_testfile", "ues10_result.txt", results_list)
    test_upload(100, unencrypted_bucket_name, "10mb_testfile", "uu10_result.txt", results_list)
    test_download(100, encrypted_sse_kms_bucket_name, "10mb_testfile", "dek10_result.txt", results_list)
    test_download(100, encrypted_sse_s3_bucket_name, "10mb_testfile", "des10_result.txt", results_list)
    test_download(100, unencrypted_bucket_name, "10mb_testfile", "du10_result.txt", results_list)
    upload_results(results_list, results_bucket_name)
    results_list = []

    create_test_file("50mb_testfile",50)
    test_upload(100, encrypted_sse_kms_bucket_name, "50mb_testfile", "uek50_result.txt", results_list)
    test_upload(100, encrypted_sse_s3_bucket_name, "50mb_testfile", "ues50_result.txt", results_list)
    test_upload(100, unencrypted_bucket_name, "50mb_testfile", "uu50_result.txt", results_list)
    test_download(100, encrypted_sse_kms_bucket_name, "50mb_testfile", "dek50_result.txt", results_list)
    test_download(100, encrypted_sse_s3_bucket_name, "50mb_testfile", "des50_result.txt", results_list)
    test_download(100, unencrypted_bucket_name, "50mb_testfile", "du50_result.txt", results_list)
    upload_results(results_list, results_bucket_name)
    results_list = []

    create_test_file("100mb_testfile",100)
    test_upload(100, encrypted_sse_kms_bucket_name, "100mb_testfile", "uek100_result.txt", results_list)
    test_upload(100, encrypted_sse_s3_bucket_name, "100mb_testfile", "ues100_result.txt", results_list)
    test_upload(100, unencrypted_bucket_name, "100mb_testfile", "uu100_result.txt", results_list)
    test_download(100, encrypted_sse_kms_bucket_name, "100mb_testfile", "dek100_result.txt", results_list)
    test_download(100, encrypted_sse_s3_bucket_name, "100mb_testfile", "des100_result.txt", results_list)
    test_download(100, unencrypted_bucket_name, "100mb_testfile", "du100_result.txt", results_list)
    upload_results(results_list, results_bucket_name)
    results_list = []



def upload_to_bucket(file, bucket):
    s3.meta.client.upload_file(file,bucket,file)

def download_from_bucket(file,bucket):
    s3.Bucket(bucket).download_file(file,file)

def test_upload(count, bucket, file, output, results_list):
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

def test_download(count, bucket, file, output, results_list):
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

main()
