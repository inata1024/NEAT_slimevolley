# 第十二次成功
编号： success12
其实是失败了
Best Fit 4.99
 
## config
与第四次设置一样。 有趣的是，最开始进化出了abs激活，表现很差。之后变成了全连接。
只使用存活奖励


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


