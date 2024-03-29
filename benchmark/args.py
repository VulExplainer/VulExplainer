"""
FileName: args.py
Description: All Hyper Arguments here.
Time: 2020/7/28 13:10
Project: GNN_benchmark
Author: Shurui Gui
"""

from tap import Tap
from typing_extensions import Literal
from typing import List, Tuple, Dict
from definitions import ROOT_DIR
import torch, os


class GeneralArgs(Tap):
    random_seed: int = 123              # fixed random seed for reproducibility
    task: Literal['train', 'test', 'explain', 'table'] = 'explain' # running mode
    dataset_split: List[float] = [0.8, 0.1, 0.1]    # train_val_test split
    train_bs: int = 3000                 # batch size for training
    val_bs: int = 3000                   # batch size for validation
    test_bs: int = 3000                  # batch size for test
    x_bs: int = 1                        # batch size for explain
    dataset_name: str = 'devign'              # dataset
    model_name: str = 'GCN_simplify2'  # specify model name
    explainer: str = 'MyVulExplainer'
    dataset_type: Literal['nlp', 'mol'] = 'mol'  # dataset type
    model_level: Literal['node', 'line', 'graph'] = 'graph'  # model level
    task_type: Literal['bcs', 'mcs', 'reg-l1'] = 'bcs'      # task type: b/m classification or regression
    target_idx: int = 0  # choose one target from multi-target task
    email: bool = False                 # email you after process down please use mail_setting.json
    explain_idx: int = 0                # default explain_idx 0
    log_file: str = 'pipeline.log'      # log file, root_dir: ROOT_DIR/log

    def add_arguments(self) -> None:
        pass


    def process_args(self) -> None:
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.dataset_name = self.dataset_name.lower()


class TrainArgs(GeneralArgs):

    tr_ctn: bool = False                    # flag for training continue
    ctn_epoch: int = 0                      # start Epoch for continue training
    lr: float = 0.005                        # learning rate
    mile_stones: List[int] = [500]
    weight_decay: int = 5e-4                # weight decay
    epoch: int = 20                       # Epochs to stop training
    val_gap: int = 100                      # do validation after val_gap batches training
    ckpt_dir: str = None                    # checkpoint dir for saving ckpt files
    save_gap: int = 10                      # how long to save a epoch

    def process_args(self) -> None:
        super().process_args()
        if self.ckpt_dir == None:
            '''self.ckpt_dir = os.path.join(ROOT_DIR, 'checkpoints',
                                         self.dataset_name, self.model_name,
                                         str(self.target_idx))'''
            self.ckpt_dir = '/home/mytest/nvd/only_nvd_output/models2/nvd-8-75.01018053481742-69.44905409890475-DevignModel_2d.ckpt'


class ValArgs(GeneralArgs):
    pass                      # batch size for validation


class TestArgs(GeneralArgs):
    test_ckpt: str = None                   # path of model checkpoint

    def process_args(self) -> None:
        super().process_args()
        if self.test_ckpt == None:
            '''self.test_ckpt = \
                os.path.join(ROOT_DIR, 'checkpoints', self.dataset_name,
                             self.model_name, str(self.target_idx),
                             f'{self.model_name}_best.ckpt')'''
        
            # self.test_ckpt = '/home/VulGnnExp/train_data/models/devign/devign52.79_53.54_75.31_62.59.ckpt'
            self.test_ckpt = '/home/VulGnnExp/train_data/models/ivdetect/ivdetect52.35_53.64_74.69_62.44.ckpt'
            # self.test_ckpt = '/home/VulGnnExp/train_data/models/reveal/deepwukong52.99_54.4_70.0_61.22.ckpt'
            # self.test_ckpt = '/home/VulGnnExp/train_data/models/deepwukong/deepwukong52.48_53.91_71.34_61.41.ckpt'

            # self.test_ckpt = '/home/VulGnnExp/train_data/models/deepwukong_mod/deepwukong_51.71_53.23_73.52_61.75.ckpt'
            # self.test_ckpt = '/home/VulGnnExp/train_data/models/ivdetect_mod/ivdetect51.71_53.4_70.0_60.58.ckpt'
            # self.test_ckpt = '/home/VulGnnExp/train_data/models/reveal_mod/reveal53.08_54.19_74.35_62.69.ckpt'
            # self.test_ckpt = '/home/VulGnnExp/train_data/models/devign_mod/devign52.42_52.86_76.59_62.55.ckpt'

class XArgs(TestArgs):
    vis: bool = False
    lr: float = 0.01
    epoch: int = 100
    sparsity: float = 0.95
    walk: bool = False
    debug: bool = False
    nolabel: bool = False
    list_sample: bool = False
    save_fig: bool = False


class DataArgs(GeneralArgs):
    dim_node: int = 0                       # Default: invalid num
    dim_edge: int = 0                       # Default: invalid num
    num_targets: int = 0                        # Default: invalid num
    dim_hidden: int = 300                   # node hidden feature's dimension
    dim_ffn: int = 300                      # final linear layer dim


common_args = GeneralArgs().parse_args(known_only=True)
data_args = DataArgs().parse_args(known_only=True)
train_args = TrainArgs().parse_args(known_only=True)
val_args = ValArgs().parse_args(known_only=True)
test_args = TestArgs().parse_args(known_only=True)
x_args = XArgs().parse_args(known_only=True)
