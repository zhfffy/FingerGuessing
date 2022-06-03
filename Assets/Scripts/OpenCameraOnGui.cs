using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using System.Threading;

public class OpenCameraOnGui : MonoBehaviour
{
    public RawImage rawImage;//相机渲染的UI
    //public GameObject quad;//相机渲染的GameObject
    private WebCamTexture webCamTexture;

    public GameObject LoadImage;//LoadingImage

    /*
    void OnGUI()
    {
        if (GUILayout.Button("OpenCamera", GUILayout.Width(200), GUILayout.Height(50))) 
        {
            ToOpenCamera();
        }
            
        if (GUILayout.Button("PauseCamera", GUILayout.Width(200), GUILayout.Height(50)))
        {
            ToPauseCamera();
        }
        //if(webCamTexture!=null) GUI.DrawTexture(new Rect(200, 200, 200, 180), webCamTexture);    
    }
    */

    // open camera
    public void ToOpenCamera()
    {
        StartCoroutine("OpenCamera");
    }

    public void ToPauseCamera()
    {
        // show LoadingImage
        LoadImage.SetActive(true);

        //OnApplicationPause(true);

        StartCoroutine(getTexture2d());
    }

    public IEnumerator OpenCamera()
    {
        int maxl = Screen.width;
        if (Screen.height > Screen.width)
        {
            maxl = Screen.height;
        }
 
        // 申请摄像头权限
        //发起使用相机设备权限的请求
        yield return Application.RequestUserAuthorization(UserAuthorization.WebCam);
        //如果请求授权成功
        if (Application.HasUserAuthorization(UserAuthorization.WebCam))
        {
            if (webCamTexture != null)  webCamTexture.Stop();
 
            //打开渲染图
            if (rawImage != null)   rawImage.gameObject.SetActive(true);

            //if (quad != null) quad.gameObject.SetActive(true);
 
            // 监控第一次授权，是否获得到设备（因为很可能第一次授权了，但是获得不到设备，这里这样避免）
            // 多次 都没有获得设备，可能就是真没有摄像头，结束获取 camera
            int i = 0;
            while (WebCamTexture.devices.Length <= 0 && 1 < 300)
            {
                yield return new WaitForEndOfFrame();
                i++;
            }

            //获取相机设备。有的设备有多个相机，所以这里返回的是个数组
            WebCamDevice[] devices = WebCamTexture.devices;
            if (WebCamTexture.devices.Length <= 0)
            {
                Debug.LogError("没有摄像头设备，请检查");
            }
            else
            {
                //print(WebCamTexture.devices.Length);
                string devicename = devices[0].name;
                //生成一张相机实时渲染的纹理图
                webCamTexture = new WebCamTexture(devicename, maxl/2, maxl == Screen.height ? Screen.width : Screen.height, 30)
                {
                    wrapMode = TextureWrapMode.Repeat
                };
 
                //将相机画面渲染的UI的RawImage或Gameobject上
                if (rawImage != null)
                {
                    //rawImage.color = Color.white;
                    rawImage.texture = webCamTexture;
                    //rawImage.GetComponent<RectTransform>().Scale.x = -1;
                    //print(devicename);
                }
                //if (quad != null) quad.GetComponent<Renderer>().material.mainTexture = webCamTexture;

                //开始渲染
                webCamTexture.Play();
            }
 
        }
        else {
            Debug.LogError("未获得读取摄像头权限");
        }
    }

    private void OnApplicationPause(bool pause)
    {
        // 应用暂停的时候暂停camera，继续的时候继续使用
        if (webCamTexture !=null)
        {
            if (pause)
            {
                webCamTexture.Pause();
            }
            else
            {
                webCamTexture.Play();
            }
        }
        
    }

    private void OnDestroy()
    {
        if (webCamTexture != null)
        {
            webCamTexture.Stop();
        }
    }

    IEnumerator getTexture2d()
    {
        yield return null;
        //只在每一帧渲染完成后才读取屏幕信息
        yield return new WaitForEndOfFrame();
        
        //实例化一张你到透明通道的大小为300*300的贴图
        Texture2D t = new Texture2D(245, 245, TextureFormat.RGB24, false);//要保存图片的大小

        //截取的区域
        t.ReadPixels(new Rect(143, 46, 245, 245), 0, 0, false);
        t.Apply();
        
        //把图片数据转换为byte数组
        byte[] byt = t.EncodeToPNG();
        
        //然后保存为图片
        //File.WriteAllBytes(Application.dataPath + "/Results/" + Time.time + ".jpg", byt);
        File.WriteAllBytes(Application.dataPath + "/Results/" + "gesture.jpg", byt);

        GameObject.Find("ScriptsHolder").GetComponent<UnityCallPython>().CallPythonGesRec();

        //yield return new WaitForSeconds(5.0f);
    }
}
