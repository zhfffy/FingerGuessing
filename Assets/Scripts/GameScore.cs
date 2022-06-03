using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class GameScore
{
    public static int NumOfMatches = 9;
    public static int PlayerScore = 0;
    public static int CPUerScore = 0;

    public static GestureEnum playerState = GestureEnum.Unknown;
    public static GestureEnum CPUState = GestureEnum.Unknown;

    public static void ResetScore()
    {
        PlayerScore = 0;
        CPUerScore = 0;
        playerState = GestureEnum.Unknown;
        CPUState = GestureEnum.Unknown;
    }
}
