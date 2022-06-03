using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SettingScene : MonoBehaviour
{
    
    //进入开始界面
    public void BackStartGame()
    {
        Utils.SwitchAndLoadScene(0);
    }
    
    [SerializeField]
    InputField GestureInput;
    [SerializeField]
    Slider NumOfMatch;
    [SerializeField]
    Text NumOfMatchText;

    public GameObject button;

    void Start()
    {
        init();
        //button.SetActive(false);//隐藏物体
        NumOfMatch.onValueChanged.AddListener((value)=>
        {
            NumOfMatchText.text = ((int)value).ToString();
        }
        );
    }

    private void init()
    {
        GestureInput.text = KeyCode.Space.ToString();
        NumOfMatch.value = GameScore.NumOfMatches;
        NumOfMatchText.text = GameScore.NumOfMatches.ToString();
    }

    public void ConfirmSetting()
    {
        // 保存默认回合次数
        GameScore.NumOfMatches = (int)NumOfMatch.value;
        //Utils.SwitchAndLoadScene(0);

        //button.selected = false;
    }


}
