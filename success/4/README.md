# 第四次成功
编号： success4
有概率击败内置agent
Best Fit 11.45 除去10的存活得分，统计意义上可以击败
 
## config
只使用存活奖励
与第三次的不同在于：不指定激活函数。用于观察网络进化、最终选择的激活函数。以及验证不指定激活函数，收敛更快。
因为操作失误，success4的stats被覆盖了，其他还好。

    slimevolley_multibinary = Game(env_name='SlimeVolley_MultiBinary',
      actionSelect='slime',
      input_size=6,
      output_size=2,
      time_factor=0,
      layers=[20, 20],
      i_act=np.full(6,1),  # Linear activation for input layer
      h_act=[1,2,3,4,5,6,7,8,9,10],  # All activation functions available for hidden layers
      o_act=np.full(2,1),   # Linear activation for output layer
      weightCap = 2.0,
      noise_bias=0.0,
      output_noise=[False, False, False],
      max_episode_length = 3000,
      in_out_labels = ['x_agent','y_agent','rel_ball_x','rel_ball_y',
                      'rel_ball_vx','rel_ball_vy',
                      'forward/back','jump']

    )


