using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StartScene : MonoBehaviour
{
    //进入游戏界面
    public void LoadGame()
    {
        Utils.SwitchAndLoadScene(1);
    }

    // 进入设置界面
    public void LoadSettingGame()
    {
        Utils.SwitchAndLoadScene(3);
    }

    public void ExitGame()
    {
        Utils.EndApp();
    }
}
