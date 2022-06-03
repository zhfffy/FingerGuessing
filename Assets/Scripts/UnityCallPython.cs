using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;


// Unity 直接调用 Python
public class UnityCallPython : MonoBehaviour
{
    string basePath = System.Environment.CurrentDirectory.Replace(" ","\" \"");
    //string basePath = @"D:\Users\Owner\Desktop\project\FingerGuessing\";

    // Start is called before the first frame update
    void Start()
    {
        //CallPythonAddHW(basePath+ "AddHelloWorld.py", 1.0f, 2.0f);
    }

    public void CallPythonAddHW(string pyScriptPath, float a, float b)
    {
        CallPythonBase(pyScriptPath,a.ToString(),b.ToString());
    }

    public void CallPythonGesRec()
    {
        CallPythonBase(basePath + @"\FingerGuessingModel\fingerPredictUnity.py");
    }

    // <param name="pyScriptPath">python 脚本路径</param>
    // <param name="argvs">python 函数参数</param>
    public void CallPythonBase(string pyScriptPath, params string[] argvs) {
        Process process = new Process();
 
        // python 的解释器位置 python.exe
        process.StartInfo.FileName = @"D:\anaconda3\python.exe";
 
        // 判断是否有参数（也可不用添加这个判断）
        if (argvs != null)
        {
            // 添加参数 （组合成：python xxx/xxx/xxx/test.python param1 param2）
            foreach (string item in argvs)
            {
                pyScriptPath += " " + item;
            }
        }
        UnityEngine.Debug.Log(pyScriptPath);
 
        process.StartInfo.UseShellExecute = false;
        process.StartInfo.Arguments = pyScriptPath;     // 路径+参数
        process.StartInfo.RedirectStandardError = false;
        process.StartInfo.RedirectStandardInput = true;
        process.StartInfo.RedirectStandardOutput = true;
        process.StartInfo.CreateNoWindow = true;        // 不显示执行窗口
 
        // 开始执行，获取执行输出，添加结果输出委托
        process.Start();
        process.BeginOutputReadLine();
        process.OutputDataReceived += new DataReceivedEventHandler(GetData);
        process.WaitForExit();
    }

    // 输出结果委托
    // <param name="sender"></param>
    // <param name="e"></param>
    void GetData(object sender, DataReceivedEventArgs e){
        // 结果不为空才打印
        if (string.IsNullOrEmpty(e.Data)==false)
        {
            if(e.Data.Length == 1){
                //UnityEngine.Debug.Log("The result is:  " + e.Data);
                //UnityEngine.Debug.Log(int.Parse(e.Data));

                if (int.Parse(e.Data) == 0) 
                    GameScore.playerState = GestureEnum.Scissor;
                else if (int.Parse(e.Data) == 1) 
                    GameScore.playerState = GestureEnum.Rock;
                else     
                    GameScore.playerState = GestureEnum.Paper;
                UnityEngine.Debug.Log("playerState is ");
                UnityEngine.Debug.Log(GameScore.playerState);                    
            }
            else
                UnityEngine.Debug.Log(e.Data);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
