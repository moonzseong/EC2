import boto3

def compare_faces(sourceFile, targetFile):

    result = ""

    client = boto3.client('rekognition')
    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')
    response = client.compare_faces(SimilarityThreshold=0,  # 유사도, 민감도
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = faceMatch['Similarity']
        result = f"동일 인물일 확률 : {similarity:.2f}%"
        result += "<br/>" # 사진에 인물이 2명이상 일경우 2번 출력되기 때문에 enter로 구분.

    imageSource.close()
    imageTarget.close()

    return result





def main():

    source_file = 'gy.jpeg'
    target_file = 'moon2.png'
    face_matches = compare_faces(source_file, target_file)
    print("Face matches: " + str(face_matches))


def detect_labels_local_file(photo):
    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    result=[]
    for label in response['Labels']:

        Name = label["Name"]
        Confidence = label["Confidence"]

        result.append(f"{Name}일 확률은 {Confidence : .2f}%입니다")

    # 구분자(<br.>)
    return "<br/>".join(map(str, result))