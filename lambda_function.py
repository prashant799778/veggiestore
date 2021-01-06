
import uuid
import pymysql
import logging
import databasefile
import uuid
import json
from pyfcm import FCMNotification
import requests
import connection
import pytz
from datetime import datetime,timedelta
import stripe
Accesskey="Qbq5MV8XLWWB5+hOgYLZbXxqIJt47Ub3y96RHXE9"
BucketName="uplad-documents"
AcessId="AKIA2W4VA3GE5OVQ5TWQ"

import boto3
import base64
s3=boto3.client("s3",aws_access_key_id=AcessId,aws_secret_access_key=Accesskey)







logger = logging.getLogger()
logger.setLevel(logging.INFO)

class d(dict):
    def __str__(self):
        return json.dumps(self)
    def __repr__(self):
        return json.dumps(self)








def CurrentDatetime():
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(tz=ist)
    ist_f_time = str(ist_time.strftime("%Y-%m-%d %H:%M:%S"))

    return ist_f_time        



def DecodeInputdata(data):
    data = json.loads(data.decode("utf-8"))                 
    return data


def CreateHashKey(FirstKey,SecoundKey):
    # hash = hashlib.sha256()
    # hash.update(('%s%s' % (FirstKey,SecoundKey)).encode('utf-8'))
    Hashkey = uuid.uuid1()

    return Hashkey


def DecodeInputdata(data):
    data = json.loads(data.decode("utf-8"))                 
    return data














def lambda_handler(event, context):
    
    logger.info(event)
    logger.info(context)
    if event['path'] == "/shopkeeperlogin":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            email=i['email']
            password=i['password']
            
           
            column="email,password,shopkeeperId,name,shoppicture"
            WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
            data = databasefile.SelectQuery("shopkeeper",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    shoppicture=i['shoppicture']
                    if (shoppicture == None) or (shoppicture == ""):
                        i['shoppicture']="https://uplad-documents.s3.ap-south-1.amazonaws.com/shoppicture/defaultuser.jpg"
                    k=d(i)


                    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

                    a=stripe.Token.create(
                      pii={"id_number": i['shopkeeperId']},
                    )

                    asjj={}
                    asjj['token']=a['id'] +str(a['id'][::-1])+str(a['id'][::-6])+str(a['id'][::-1])+str(a['id'][::-5])+str(a['id'][::-2])+str(a['id'][::-3])+str(a['id'][::-4])
                    print(asjj)
                    asjj['shopkeeperId']=data['result'][0]['shopkeeperId']
                    asjj['shoppicture']=data['result'][0]['shoppicture']

                    WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
                    column="token ='"+ str(asjj['token'])+"'"
                    data = databasefile.UpdateQuery("shopkeeper",column,WhereCondition)

               
                hpp=d(asjj)
                hpp["status"]=1
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps(hpp)}
            else:

                return {'statusCode':201,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'Wrong password and email ,Please Enter Correct Credentails','status':0})}
    elif event['path'] == "/shopkeeperveggieitems":
        print("www")
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            shopkeeperId=i['shopkeeperId']

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and shopkeeperId='"+str(shopkeeperId)+"'"
            data = databasefile.SelectQuery("shopkeepermaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                column = "shopkeeperId,price,veggiepicture,veggieId"
                WhereCondition=" and shopkeeperId='"+ str(shopkeeperId)+"'"
                data1=databasefile.SelectQuery("veggiestore",column,WhereCondition)
                if data1['status'] != 'false':
                    for i in data1['result']:
                        k=d(i)
                        print(k)
                        h.append(k)

                    print(h,"swwww")
                    result={'result':h}
                    print(result,"qwws")
                   



                 

                    
                    

                    
                    r=d(result)
                    t={}
                    t['result']=r['result']
                    hpp=d(t)
                    print({'statusCode':200,'body':hpp})
                    return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}
                else:
                    t={}
                    t['result']=" No items in  your store,Please add "
                    hpp=d(t)
                    print({'statusCode':200,'body':hpp})
                    return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}

    elif event['path'] == "/particularshopkeeperstore":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            shopkeeperId=i['shopkeeperId']
            h=[]
            column = "shopkeeperId,price,veggiepicture,veggieId"
            WhereCondition=" and shopkeeperId='"+ str(shopkeeperId)+"'"
            data1=databasefile.SelectQuery("veggiestore",column,WhereCondition)
            if data1['status'] != 'false':
                for i in data1['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")
                result={'result':h}
                print(result,"qwws")
               



             

                
                

                
                r=d(result)
                t={}
                t['result']=r['result']
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                t={}
                t['result']=" No items in  your store,Please add "
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}

            
                    
           
    elif event['path'] == "/userlogin":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            email=i['email']
            password=i['password']
            
           
            column="email,password,userId,name"
            WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
            data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)

                    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

                    a=stripe.Token.create(
                      pii={"id_number": i['userId']},
                    )

                    asjj={}
                    asjj['token']=a['id'] +str(a['id'][::-1])+str(a['id'][::-6])+str(a['id'][::-1])+str(a['id'][::-5])+str(a['id'][::-2])+str(a['id'][::-3])+str(a['id'][::-4])
                    print(asjj)
                    WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
                    column="token ='"+ str(asjj['token'])+"'"
                    data = databasefile.UpdateQuery("usermaster",column,WhereCondition)

               
                hpp=d(asjj)
                hpp['status']=1
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps({'result':'Wrong password and email ,Please Enter Correct Credentails','status':0})}
            
    elif event['path'] == "/userdashboard":
        print("www")
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")

                u="ww"
                result={'result':h}
                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r['result']
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps(hpp)}
            else:
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    
    elif event['path'] == "/shopkeeperregistration":
        
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            name=i['name']
            email=i['email']
            password=i['password']
            phone=i['phone']
           
            address=i['address']
            shopkeeperId=CreateHashKey(name,email)
            flag="i"
            WhereCondition = " and name = '" + str(name)+"' or email='"+str(email)+"'"
            count = databasefile.SelectCountQuery("shopkeeper",WhereCondition,"")
            if int(count) > 0:
                t={}
                t['result'] ="Shopkeeper Already  exist "
                hpp=d(t)
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
                
            else:
                if flag =="i":
                    print("11111111111111111111111")
                    s=CurrentDatetime()
                    
                    column = "shopkeeperId,name,address,phone,password,email,registime"                
                    values = " '" + str(shopkeeperId)  + "','" + str(name) + "','" + str(address) + "','" + str(phone) + "','" + str(password)  + "','" + str(email) + "','" + str(s)  + "' "
                    data = databasefile.InsertQuery("shopkeeper",column,values)       
                    if data != "0":

                        column =  "shopkeeperId,name,address,phone,password,email,registime"
                        data = databasefile.SelectQuery("shopkeeper",column,WhereCondition,"","","")
                        hhh=[]
                        for i in data['result']:
                            k=d(i)
                            print(k)
                            hhh.append(k)

                        
                        print(hhh,"swwww")


                        u="ww"
                        result={'result':hhh}
                        print(result,"qwws")
                        r=d(result)
                        t={}
                        t['result']=r['result']
                        hpp=d(t)
                        print({'statusCode':200,'body':hpp})
                        return {'statusCode':200,'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                        },'body':json.dumps(hpp)}
   
                    
                    

                        
                   
    elif event['path'] == "/userregistration":
        
        if event['httpMethod'] == "POST":
            

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            name=i['name']
            email=i['email']
            password=i['password']
            phone=i['phone']
            address=i['address']
           

            

           

            userId=CreateHashKey(name,email)
            

            flag="i"
            
            WhereCondition = " and name = '" + str(name)+"' or email='"+str(email)+"'"
            count = databasefile.SelectCountQuery("usermaster",WhereCondition,"")
            if int(count) > 0:
                t={}
                t['result'] ="user Already  exist "
                hpp=d(t)
                return {'statusCode':201,'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                      },'body':json.dumps(hpp)}
                
            else:
                if flag =="i":
                    print("11111111111111111111111")
                    s=CurrentDatetime()
                    
                    column = "userId,name,address,phone,password,email,registime"                
                    values = " '" + str(userId)  + "','" + str(name) + "','" + str(address) + "','" + str(phone) + "','" + str(password)  + "','" + str(email) + "','" + str(s)+ "'"
                    data = databasefile.InsertQuery("usermaster",column,values)  
                    WhereCondition="and userId='"+str(userId)+"'"     
                    if data != "0":

                        column = 'name,userId,address,phone,email,registime'
                        data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
                        hhh=[]
                        for i in data['result']:
                            k=d(i)
                            print(k)
                            hhh.append(k)

                        
                        print(hhh,"swwww")


                        u="ww"
                        result={'result':hhh[0]}
                        print(result,"qwws")
                        r=d(result)
                        t={}
                        t['result']=r['result']
                        hpp=d(t)
                        print({'statusCode':200,'body':hpp})
                        return {'statusCode':200,'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                      },'body':json.dumps(hpp)}
            

        else:
            
            column = 'name,userId,address,phone,email,registime'
            data = databasefile.SelectQuery("usermaster",column,"","","","")
            hhh=[]
            for i in data['result']:
                k=d(i)
                print(k)
                hhh.append(k)

            
            print(hhh,"swwww")


            u="ww"
            result={'result':hhh}
            print(result,"qwws")
            r=d(result)
            t={}
            t['result']=r['result']
            hpp=d(t)
            print({'statusCode':200,'body':hpp})
            return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },'body':json.dumps(hpp)}
    
        
    elif event['path'] == "/adminlogin":
        print("www")
        if event['httpMethod'] == "POST":
            
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            email=i['email']
            password=i['password']
            
           
            column="email,adminId"
            WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)

                    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

                    a=stripe.Token.create(
                      pii={"id_number": i['adminId']},
                    )

                    asjj={}
                    asjj['token']=a['id'] +str(a['id'][::-1])+str(a['id'][::-6])+str(a['id'][::-1])+str(a['id'][::-5])+str(a['id'][::-2])+str(a['id'][::-3])+str(a['id'][::-4])
                    print(asjj)
                    asjj['adminId']=i['adminId']
                    WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
                    column="token ='"+ str(asjj['token'])+"'"
                    data = databasefile.UpdateQuery("adminmaster",column,WhereCondition)

               
                hpp=d(asjj)
                hpp['status']=1
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}
            else:
                return {'statusCode':200,'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                        },'body':json.dumps({'result':'Wrong password and email ,Please Enter Correct Credentails','status':0})}

    
    elif event['path'] == "/admindashboard":
        print("www")
        if event['httpMethod'] == "POST":
            
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

           
            
           
            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")

                u="ww"
                result={'result':h}
                print(result,"qwws")
                r=d(result)
                t={}
                t['result']={"completed":8,"pending":2,"rejected":3,"agent":14}
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps(hpp)}
            else:
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    
   

    elif event['path'] == "/allshopkeepers":
        
        if event['httpMethod'] =="GET":
            
            column = 'id,shopkeeperId,name,address,phone,email,shoppicture,registime'
            data = databasefile.SelectQuery("shopkeeper",column,"","","","")
            hhh=[]
            for i in data['result']:
                shoppicture=i['shoppicture']
                if (shoppicture == None) or (shoppicture == ""):
                    i['shoppicture']='https://uplad-documents.s3.ap-south-1.amazonaws.com/shoppicture/defaultuser.jpg'
                
                k=d(i)
                print(k)
                hhh.append(k)
 
            
            print(hhh,"swwww")


            u="ww"
            result={'result':hhh}
            print(result,"qwws")
            r=d(result)
            t={}
            t['result']=r['result']
            hpp=d(t)
            print({'statusCode':200,'body':hpp})
            return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },'body':json.dumps(hpp)}

    
    elif event['path'] == "/uploadveggiepicture":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            shopkeeperId=i['shopkeeperId']
            veggiepicture=i['veggiepicture']
            price=i['price']
            i=0
            u=CreateHashKey(shopkeeperId,price)
            
            

            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and shopkeeperId='"+str(shopkeeperId)+"'"
            data = databasefile.SelectQuery("shopkeeper",column,WhereCondition,"","","")
            if data['status']!='false':
                print("ss")

                
                panCardId1="veggiepicture"+str(u)
                panCard1=veggiepicture[veggiepicture.find(",")+1:]
               
                dec3=base64.b64decode(panCard1+"===")

                
                a6=veggiepicture.split("data:")
                a7=a6[1].split("/")
                a8=a7[1].split(";")
                print(a8,"a8")

                pancardextension=a8[0]
                
                panCardId000=panCardId1+"."+str(pancardextension)
               
                path_test3="veggiepicture"
               
                panCardfileName=path_test3+"/"+str(panCardId000)
                link="https://uplad-documents.s3.ap-south-1.amazonaws.com/"
                picture=link+"/"+panCardfileName
               
                ip1=s3.put_object(Bucket=BucketName,Key=panCardfileName,Body=dec3)
                column = "shopkeeperId,price,veggiepicture,veggieId"                
                values = " '" + str(shopkeeperId)  + "','" + str(price) + "','" + str(picture)  + "','" + str(veggieId)+ "' "
                data = databasefile.InsertQuery("veggiestore",column,values)








               
                t={}
                t['result']="upload Successfully"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}
            else:
                t={}

                t['result']="shopkeeper token is Wrong"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':301,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}
    elif event['path'] == "/uploadshoppicture":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            shopkeeperId=i['shopkeeperId']
            shoppicture=i['shoppicture']
           
            
            

            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and shopkeeperId='"+str(shopkeeperId)+"'"
            data = databasefile.SelectQuery("shopkeeper",column,WhereCondition,"","","")
            if data['status']!='false':
                print("ss")
                
                
                panCardId1="shoppicture"+str(shopkeeperId)
                panCard1=shoppicture[shoppicture.find(",")+1:]
               
                dec3=base64.b64decode(panCard1+"===")

                
                a6=veggiepicture.split("data:")
                a7=a6[1].split("/")
                a8=a7[1].split(";")
                print(a8,"a8")

                pancardextension=a8[0]
                
                panCardId000=panCardId1+"."+str(pancardextension)
               
                path_test3="shoppicture"
               
                panCardfileName=path_test3+"/"+str(panCardId000)
                link="https://uplad-documents.s3.ap-south-1.amazonaws.com/"
                picture=link+"/"+panCardfileName
               
                ip1=s3.put_object(Bucket=BucketName,Key=panCardfileName,Body=dec3)
                column = "shoppicture='"+str(picture)+"'"
                WhereCondition=" and shopkeeperId='"+str(shopkeeperId)+"'"                
               
                data = databasefile.UpdateQuery("shopkeeper",column,WhereCondition)








               
                t={}
                t['result']="upload Successfully"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}
            else:
                t={}

                t['result']="shopkeeper token is Wrong"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':301,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}
    elif event['path'] == "/updateveggieprice":
        print("www")
        
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            price=i['price']
            shopkeeperId=i['shopkeeperId']
            veggieId=i['veggieId']
           

        
            
            column="price='" +str(price)+ "'"
            whereCondition= "  and veggieId = '" + str(veggieId)+ "' and shopkeeperId='"+str(shopkeeperId)+"'"
            output=databasefile.UpdateQuery("amountoption",column,whereCondition)
                       
            if output!='0':
                t={ }
                t['result']='Price updated Successfully'
                hpp=d(t)
                                    
                return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
                        
           
                        

                        
                   

           

    
    
    elif event['path'] == "/emailverfication":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            userId=i['agentId']

            print(userId)
            
            column="emailverfication='" +str(1)+ "'"
            whereCondition= "  and agentId = '" + str(userId)+ "' "
            output=databasefile.UpdateQuery("agentmaster",column,whereCondition)
                       
            if output!='0':
                t={ }
                t['result']='verified Successfully'
                hpp=d(t)
                                    
                return {'statusCode':200,'body':json.dumps(hpp)}
    
    elif event['path'] == "/mobileverfication":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            userId=i['agentId']

            print(userId)
            
            column= "mobileverfication='" +str(1)+ "'"
            whereCondition = "  and agentId = '" + str(userId)+ "' "
            output=databasefile.UpdateQuery("agentmaster",column,whereCondition)
                       
            if output!='0':
                t={ }
                t['result']='verified Successfully'
                hpp=d(t)
                                    
                return {'statusCode':200,'body':json.dumps(hpp)}




    else:
        print("qwqw")
        