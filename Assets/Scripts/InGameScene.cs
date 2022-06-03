using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class InGameScene : MonoBehaviour
{
    [SerializeField]
    Text CPUScore, playerScore;
    [SerializeField]
    Image CpuMoveImage, PlayerMoveImage;
    [SerializeField]
    Sprite RImg, PImg, SImg, DefaultImg;

    public GameObject LoadImage;

    private int currnetIndex = 0;
    //private bool isProcessing = false;

    private void Start()
    {
        DisplayDefaultScore();
        LoadImage.SetActive(false);
    }

    void DisplayDefaultScore()
    {
        CPUScore.text = GameScore.CPUerScore.ToString();
        playerScore.text = GameScore.PlayerScore.ToString();
    }

    private void Update(){
        //UnityEngine.Debug.Log("playerState is ");
        //UnityEngine.Debug.Log(GameScore.playerState);
        //UnityEngine.Debug.Log(currnetIndex);

        if (currnetIndex < GameScore.NumOfMatches)
        {
            if (GameScore.playerState != GestureEnum.Unknown)
            {

                CPUProcessGame();

                LoadImage.SetActive(false);

                currnetIndex++;

                Invoke("EndProcessing", 2);
            }
        }
        else // 游戏结束
        {
            Invoke("LoadGameOver", 3);
            Utils.SwitchAndLoadScene(2);
        }
    }

    private void CPUProcessGame()
    {
        //随机出一个牌
        GameScore.CPUState = (GestureEnum)UnityEngine.Random.Range(0, 3);

        //显示牌型
        DisplayGesture(GameScore.playerState, PlayerMoveImage);
        DisplayGesture(GameScore.CPUState, CpuMoveImage);

        if(CalculateResult() == ResultEnum.Win)
        {
            GameScore.PlayerScore++;
        }
        else if (CalculateResult() == ResultEnum.Lose)
        {
            GameScore.CPUerScore++;
        }

        DisplayDefaultScore();

        GameScore.playerState = GestureEnum.Unknown;
        GameScore.CPUState = GestureEnum.Unknown;
    }

    private void DisplayGesture(GestureEnum gesture, Image img)
    {
        switch(gesture)
        {
            case GestureEnum.Scissor:
                img.sprite = SImg;
                break;
            case GestureEnum.Rock:
                img.sprite = RImg;
                break;
            case GestureEnum.Paper:
                img.sprite = PImg;
                break;
            default:
                img.sprite = DefaultImg;
                break;    
        }
    }

    private ResultEnum CalculateResult()
    {
        int substraction = GameScore.playerState - GameScore.CPUState;
        if (substraction == 0)
        {
            return ResultEnum.Tie;
        }
        else if (substraction == 1 || substraction == -2)
        {
            return ResultEnum.Win;
        }
        else
        {
            return ResultEnum.Lose;
        }
    }

    private void EndProcessing()
    {
        PlayerMoveImage.sprite = DefaultImg;
        CpuMoveImage.sprite = DefaultImg;
    }


    // 进入gameover界面
    public void LoadGameOver()
    {
        Utils.SwitchAndLoadScene(0);
        GameScore.ResetScore();
    }
}
