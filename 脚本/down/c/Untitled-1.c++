/**
 * @file LED_Control.c
 * @brief 使用定时器和按键控制LED流水灯
 * @details
 * - 使用Timer0实现500ms定时
 * - 按键k1切换LED流水方向
 * - 晶振:11.0592MHz
 */

#include <REGX52.H>
#include <INTRINS.H>

//类型重定义
#define uchar unsigned char
#define uint unsigned int 

//全局变量
uchar keyNum = 0; //按键键值
uchar LEDMode = 0; //LED模式：0=左移， 1=右移， 2=闪烁， 3=呼吸灯， 4=追逐， 5=图案， 6=随机
uchar LEDSpeed = 1; //LED速度：1=慢， 2=中， 3=快
uint speedDelay = 25; //速度对应的延时计数（20ms * speedDelay）
bit LEDPause = 0; //LED暂停标志：0=运行，1=暂停
uchar chasePos = 0; //追逐模式位置
uchar patternIndex = 0; //图案模式索引


//函数声明
void Timer0_Init(void); //定时器0初始化
uchar key(void); //按键扫描函数
void DelayMs(uint ms); //延时函数
void LED_Breathe(void); //呼吸灯效果函数
void LED_Chase(void); //追逐模式函数
void LED_Pattern(void); //图案模式函数
void LED_Random(void); //随机模式函数

/**
 * @brief 主函数
 */
 void main(void)
{
    P2 = 0xfe;             //初始状态：P2.0亮，其他灭（1111 1110）
    Timer0_Init();        //初始化定时器0
  
    while(1)             //主循环
    {
        keyNum = key(); //获取按键值

        if(keyNum)      //如果有按键按下
        {
            if(keyNum == 1) //如果k1按键按下：切换模式
            {
                LEDMode ++; //模式切换
                if(LEDMode >= 7) //0-6七种模式
                {
                    LEDMode = 0; 
                }
                //模式切换时重置相关参数
                chasePos = 0;
                patternIndex = 0;
            }
            else if(keyNum == 2) //如果k2按键按下：切换速度
            {
                LEDSpeed ++; //速度切换
                if(LEDSpeed >= 4) //1-3三种速度
                {
                    LEDSpeed = 1; 
                }
                //根据速度设置延时
                switch(LEDSpeed)
                {
                    case 1: speedDelay = 25; break; //慢：500ms
                    case 2: speedDelay = 10; break; //中：200ms
                    case 3: speedDelay = 5; break;  //快：100ms
                }
            }
            else if(keyNum == 3) //如果k3按键按下：暂停/继续
            {
                LEDPause = !LEDPause; //切换暂停状态
                if(LEDPause)
                {
                    P2 = 0xff; //暂停时全灭
                }
                else
                {
                    P2 = 0xfe; //继续时从初始状态开始
                }
            }
            else if(keyNum == 4) //如果k4按键按下：重置
            {
                LEDMode = 0; //重置为初始模式
                LEDSpeed = 1; //重置为初始速度
                LEDPause = 0; //重置为运行状态
                speedDelay = 25; //重置延时
                chasePos = 0; //重置追逐位置
                patternIndex = 0; //重置图案索引
                P2 = 0xfe; //重置为初始状态
            }
        }
    }   
}

    /**
     * @brief 定时器0初始化
     * @note 使用11.0592MHz晶振,定时20ms
    */
    void Timer0_Init(void)
{
    TMOD &= 0xF0; //清除Timer0位
    TMOD |= 0x01; //设置Timer0为模式1 （16位定时器）
    
    //计算20ms定时初值(11.0592MHz)
    //机器周期 = 12 / 11.0592MHz  ≈ 1.085μs
    //20ms = 20000μs, 需要计数值 = 20000 / 1.085  ≈ 18432
    // 初值 = 65536 - 18432 = 47104 =0xB800
    TH0 = 0xB8;   //高8位：0xB8 = 184
    TL0 = 0x00;   //低8位：0x00 = 0

    TF0 = 0;       //清除溢出标志
    ET0 = 1;      //允许Timer0中断
    EA = 1;       //开总中断
    TR0 = 1;      //启动定时器
}

/**
 * @brief 定时器0中断服务函数
 * @note 每20ms中断一次,通过计数实习500ms定时
 */
void Timer0_ISR(void) interrupt 1
{
    static uint T0Count = 0; //中断次数计数器

    // 重新装入初值(20ms定时)
    TH0 = 0xB8;          //高8位
    TL0 = 0x00;          //低8位
    
    T0Count ++;              //中断次数加1

    if(T0Count >= speedDelay)        //根据速度设置延时
        {
            T0Count = 0;    //计数器清零

            // 检查是否暂停
            if(!LEDPause)
            {
                // 根据模式控制LED流动
                if(LEDMode == 0)         //模式0:左移
                {
                    P2 = _crol_(P2,1); //循环左移一位
                }
                else if(LEDMode == 1)    //模式1:右移
                {
                    P2 = _cror_(P2,1); //循环右移一位
                }
                else if(LEDMode == 2)    //模式2:闪烁
                {
                    P2 = ~P2; //取反，实现闪烁效果
                }
                else if(LEDMode == 3)    //模式3:呼吸灯
                {
                    LED_Breathe(); //调用呼吸灯函数
                }
                else if(LEDMode == 4)    //模式4:追逐
                {
                    LED_Chase(); //调用追逐模式函数
                }
                else if(LEDMode == 5)    //模式5:图案
                {
                    LED_Pattern(); //调用图案模式函数
                }
                else if(LEDMode == 6)    //模式6:随机
                {
                    LED_Random(); //调用随机模式函数
                }   
            }
        }
}

/**
 * @brief 按键扫描函数
 * @return  按键键值: 1=k1, 2=k2, 3=k3, 4=k4, 0=无按键
 */
 uchar key(void)
{
    uchar keyNum = 0; 
    
    // 检测k1 (P3.1)
    if(P3_1 == 0)
    {
        DelayMs(20);                      //消抖延时
        while(P3_1 == 0);             //等待按键释放
        DelayMs(20);                    //释放消抖
        keyNum = 1;
    }

    // 检测k2 (P3.0)
    if(P3_0 == 0)
    {
        DelayMs(20);                      //消抖延时
        while(P3_0 == 0);             //等待按键释放
        DelayMs(20);                    //释放消抖
        keyNum = 2;
    }
      
    // 检测k3 (P3.2)
    if(P3_2 == 0)
    {
        DelayMs(20);                      //消抖延时
        while(P3_2 == 0);             //等待按键释放
        DelayMs(20);                    //释放消抖
        keyNum = 3;
    }

    // 检测k4 (P3.3)
    if(P3_3 == 0)
    {
        DelayMs(20);                      //消抖延时
        while(P3_3 == 0);             //等待按键释放
        DelayMs(20);                    //释放消抖
        keyNum = 4;
    }
 
    return keyNum; //返回按键键值
}

/**
 * @brief 延时函数
 * @param xms 延时时间，单位：毫秒
 * @note 粗略延时，不精确
 */
 void DelayMs(uint xms)
{
    uint i,j;
    for(i = xms; i > 0; i--)
    {
        for(j = 110; j > 0; j--);
    }
}

/**
 * @brief 呼吸灯效果函数
 * @note 通过软件PWM实现LED亮度渐变
 */
void LED_Breathe(void)
{
    static uchar brightness = 0; //亮度值：0-10
    static bit direction = 0; //方向：0=变亮，1=变暗
    static uchar cnt = 0; //计数器
    
    cnt++;
    if(cnt >= 10) //每个亮度级别持续10个周期
    {
        cnt = 0;
        
        if(direction == 0) //变亮
        {
            brightness++;
            if(brightness >= 10)
            {
                direction = 1; //开始变暗
            }
        }
        else //变暗
        {
            brightness--;
            if(brightness <= 0)
            {
                direction = 0; //开始变亮
            }
        }
    }
    
    //根据亮度控制LED
    if(brightness == 0)
    {
        P2 = 0xff; //全灭
    }
    else if(brightness == 10)
    {
        P2 = 0x00; //全亮
    }
    else
    {
        //使用软件PWM实现亮度控制
        P2 = 0x00; //点亮
        DelayMs(brightness); //亮的时间
        P2 = 0xff; //熄灭
        DelayMs(10 - brightness); //灭的时间
    }
}

/**
 * @brief 追逐模式函数
 * @note 实现单个LED追逐效果
 */
void LED_Chase(void)
{
    //追逐效果：单个LED从左到右移动
    P2 = 0xff; //全灭
    P2 &= ~(0x01 << chasePos); //点亮当前位置
    
    chasePos++;
    if(chasePos >= 8) //8个LED
    {
        chasePos = 0;
    }
}

/**
 * @brief 图案模式函数
 * @note 显示预设的LED图案
 */
void LED_Pattern(void)
{
    //预设图案数组
    uchar patterns[] = {
        0x00, //全灭
        0xff, //全亮
        0x55, //交替亮灭
        0xaa, //交替灭亮
        0x0f, //前4个亮
        0xf0, //后4个亮
        0x81, //两边亮
        0x42, //中间两边亮
        0x24, //中间亮
        0x18  //中间两边亮
    };
    
    P2 = patterns[patternIndex];
    
    patternIndex++;
    if(patternIndex >= sizeof(patterns))
    {
        patternIndex = 0;
    }
}

/**
 * @brief 随机模式函数
 * @note 随机点亮LED
 */
void LED_Random(void)
{
    static uint randSeed = 12345; //随机种子
    
    //简单的线性同余生成器
    randSeed = (randSeed * 1103515245 + 12345) % 32768;
    
    //使用随机数控制LED
    P2 = randSeed % 256; //0-255的随机值 