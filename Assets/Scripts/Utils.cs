using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Utils
{
    public static void SwitchAndLoadScene(int index)
    {
        SceneManager.LoadScene(index, LoadSceneMode.Single);
    }

    public static void EndApp()
    {
        #if UNITY_EDITOR 
            UnityEditor.EditorApplication.isPlaying = false;
            Debug.Log("编辑状态游戏退出");
        #else
            Application.Quit();
            Debug.Log("游戏退出");
        #endif    
    }
}
