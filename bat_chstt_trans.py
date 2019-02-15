# -*- coding: UTF-8 -*-
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from google.cloud import storage
from google.cloud import translate

def transcribe_gcs(gcs_uri,filename):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR',
        use_enhanced=True,
        audio_channel_count=1,
        enable_separate_recognition_per_channel=True
        )

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        resulttext = result.alternatives[0].transcript + '.\r\n'
        with open(filename,"a") as myfile:
            myfile.write(resulttext)

def trans(filename,transfilename):
    with open(filename,"r") as myfile:
        mytext=myfile.read()
    # Instantiates a client
    translate_client = translate.Client()

    # The target language
    target = 'zh-CN'

    # Translates some text into Russian
    translation = translate_client.translate(
        mytext,
        target_language=target)

    with open(transfilename,'a') as transfile:
        transfile.write(translation['translatedText'])

storage_client = storage.Client()
bucket_name = 'hwvoice'
bucket = storage_client.get_bucket(bucket_name)

blobs = bucket.list_blobs()

for blob in blobs:
    if ".wav" in blob.name:
        bloblink = "gs://hwvoice/" + blob.name
        print(bloblink)
        filename=blob.name[8:-3]+'txt'
        transfilename=blob.name[8:-4]+'-en.txt'
        print(filename)
        print(transfilename)
        transcribe_gcs(bloblink,filename)
        trans(filename,transfilename)
