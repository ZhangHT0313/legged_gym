# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class EL_MINI_TEST_Cfg( LeggedRobotCfg ):
    class env:
        num_envs = 4096
        num_observations = 66   #66 = 3+3+3+18+18+18
        num_privileged_obs = None # if not None a priviledge_obs_buf will be returned by step() (critic obs for assymetric training). None is returned otherwise 
        num_actions = 18
        env_spacing = 3.  # not used with heightfields/trimeshes 
        send_timeouts = True # send time out information to the algorithm
        episode_length_s = 20 # episode length in seconds

    class pmtg:
        gait_type = 'walk'
        duty_factor = 0.5
        base_frequency = 1.25
        max_clearance = 0.10
        body_height = 0.28
        consider_foothold = False
        z_updown_height_func = ["cubic_up", "cubic_down"]
        max_horizontal_offset = 0.0
        train_mode = True

    class terrain( LeggedRobotCfg.terrain ):
        mesh_type = 'plane'
        measure_heights = False

    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.1] # x,y,z [m]
        default_joint_angles = {
                # 左前腿 (LF)
                "LF_HAA": 0.0,    # 左前髋关节外展/内收角度
                "LF_HFE": 0.3,    # 左前髋关节屈曲/伸展角度
                "LF_KFE": 0.5,   # 左前膝关节屈曲/伸展角度

                # 左中腿 (LM)
                "LM_HAA": 0.0,    # 左中髋关节外展/内收角度
                "LM_HFE": 0.3,    # 左中髋关节屈曲/伸展角度
                "LM_KFE": 0.5,   # 左中膝关节屈曲/伸展角度

                # 左后腿 (LB)
                "LB_HAA": 0.0,    # 左后髋关节外展/内收角度
                "LB_HFE": 0.3,   # 左后髋关节屈曲/伸展角度
                "LB_KFE": 0.5,    # 左后膝关节屈曲/伸展角度

                # 右前腿 (RF)
                "RF_HAA": 0.0,   # 右前髋关节外展/内收角度
                "RF_HFE": 0.3,    # 右前髋关节屈曲/伸展角度
                "RF_KFE": 0.5,   # 右前膝关节屈曲/伸展角度

                # 右中腿 (RM)
                "RM_HAA": 0.0,   # 右中髋关节外展/内收角度
                "RM_HFE": 0.3,    # 右中髋关节屈曲/伸展角度
                "RM_KFE": 0.5,   # 右中膝关节屈曲/伸展角度

                # 右后腿 (RB)
                "RB_HAA": 0.0,   # 右后髋关节外展/内收角度
                "RB_HFE": 0.3,   # 右后髋关节屈曲/伸展角度
                "RB_KFE": 0.5,    # 右后膝关节屈曲/伸展角度
            }

    class control( LeggedRobotCfg.control ):
        # PD Drive parameters:
        stiffness = {'HAA': 40., 'HFE': 40., 'KFE': 40.}  # [N*m/rad]
        damping = {'HAA': 0.8, 'HFE': 0.8, 'KFE': 0.8}     # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.5
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4
        use_actuator_network = True
        actuator_net_file = "{LEGGED_GYM_ROOT_DIR}/resources/actuator_nets/anydrive_v3_lstm.pt"

    class asset( LeggedRobotCfg.asset ):
        file = "{LEGGED_GYM_ROOT_DIR}/resources/robots/el_mini/urdf/el_mini.urdf"
        name = "el_mini"
        foot_name = "FOOT"
        shoulder_name = "shoulder"
        penalize_contacts_on = ["RB_SHANK",
                                "LB_SHANK", 
                                "RM_SHANK",
                                "LM_SHANK",
                                "RF_SHANK",
                                "LF_SHANK",

                                "RB_THIGH",
                                "LB_THIGH",
                                "RM_THIGH",
                                "LM_THIGH",
                                "RF_THIGH",
                                "LF_THIGH"]
        terminate_after_contacts_on = ["BASE"]
        self_collisions = 1 # 1 to disable, 0 to enable...bitwise filter
        flip_visual_attachments = False

    class domain_rand( LeggedRobotCfg.domain_rand):
        randomize_base_mass1500 = True
        added_mass_range = [-5., 5.]
    
    class noise:
        add_noise = True
        noise_level = 1.0 # scales other values
        class noise_scales:
            dof_pos = 0.01
            dof_vel = 1.5
            lin_vel = 0.1
            ang_vel = 0.2
            gravity = 0.05
            height_measurements = 0.1
  
    class rewards( LeggedRobotCfg.rewards ):
        base_height_target = 1
        max_contact_force = 300.
        only_positive_rewards = True
        class scales( LeggedRobotCfg.rewards.scales ):
            pass

class EL_MINI_TEST_PPO( LeggedRobotCfgPPO ):
    class policy:
        init_noise_std = 0.5
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [512, 256, 128]
        activation = 'elu' # can be elu, relu, selu, crelu, lrelu, tanh, sigmoid
        # only for 'ActorCriticRecurrent':
        # rnn_type = 'lstm'
        # rnn_hidden_size = 512
        # rnn_num_layers = 1

    class runner( LeggedRobotCfgPPO.runner ):
        max_iterations = 1000

        # logging
        save_interval = 50 # check for potential saves every this many iterations
        experiment_name = 'el_mini_test'
        run_name = ''
        # load and resume
        resume = False
        load_run = -1 # -1 = last run
        checkpoint = -1 # -1 = last saved model
        resume_path = None # updated from load_run and chkpt
