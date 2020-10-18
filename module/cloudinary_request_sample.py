import cloudinary
import cloudinary.uploader
from pprint import pprint
 
cloudinary.config(
  cloud_name = "aichi-prefectural-university",
  api_key = "884251713832499",
  api_secret = "gVicsVp9HqJhu_Yxf7xxKDGjVTQ"
)

#res = cloudinary.uploader.upload(file="../images/im1.png", public_id="test")
#pprint(res)

url = cloudinary.CloudinaryImage("test").image(
  width=250,
  height=250,
  quality="auto",
  fetch_format="auto",
  secure=True, # HTTPS
)
print(url)

if __name__ == "__main__":
  cloudinary.config(
    cloud_name = "aichi-prefectural-university",
    api_key = "884251713832499",
    api_secret = "gVicsVp9HqJhu_Yxf7xxKDGjVTQ"
  )

  #res = cloudinary.uploader.upload(file="sample2.PNG", public_id="sample2")
  #pprint(res)

  res = cloudinary.api.resources(type="upload")
  for img in res["resources"]:
      pprint(img)


  url = cloudinary.CloudinaryImage("sample2").image(
    width=250,
    height=250,
    quality="auto",
    fetch_format="auto",
    secure=True, # HTTPS
  )
  print(url) 