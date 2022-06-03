using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Drawing;

public class GameOverScene : MonoBehaviour
{
    [SerializeField]
    Text resultGame;

    public void Start()
    {
        resultGame.text = JudgeResult();
    }

    private string JudgeResult()
    {
        if (GameScore.PlayerScore > GameScore.CPUerScore)
        {
            return "You Won! Try again you luck.";
        }
        else if (GameScore.PlayerScore < GameScore.CPUerScore)
        {
            return "You Lost. Cheer Up!";
        }
        else
        {
            return "Draw Game. Try again you luck.";
        }
    }

    public void BackStartGame()
    {
        Utils.SwitchAndLoadScene(0);
        GameScore.ResetScore();
    }

    public void ExitGame()
    {
        Utils.EndApp();
    }
}
