import ast
import torch
from model import CNNMnist, CNNCifar, CNNFashion_Mnist
from torch import nn
from utils import get_dataset


class FL:

    def __init__(self, ):
        self.options = ""
        self.weight = ""
        self.train_load = ""
        self.test_load = ""

    def initial(self, param):
        self.options = param
        train_dataset, test_dataset = get_dataset(self.options)

        self.train_load = torch.utils.data.DataLoader(train_dataset,
                                                      batch_size=self.options["local_bs"],
                                                      shuffle=True)

        self.test_load = torch.utils.data.DataLoader(test_dataset,
                                                     batch_size=self.options["local_bs"],
                                                     shuffle=False)

    def receive_weight(self, file, file_name):
        file_name = ast.literal_eval(file_name.decode("utf-8"))
        file_name = file_name['file_name']

        wfile = open(file_name, 'wb')
        wfile.write(file)
        wfile.close()

        w = torch.load(file_name)
        self.weight = w
        print("Receive")
        return None

    def update(self):
        # epoch_loss = []
        model = select_model(self.options)
        model.to('cuda')
        model.load_state_dict(self.weight)
        criterion = nn.NLLLoss().to('cuda')
        optimizer = torch.optim.SGD(model.parameters(), lr=self.options["lr"],
                                    momentum=0.5)
        model.train()
        print("Start Training")

        for iter in range(self.options["local_ep"]):
            batch_loss = []
            for batch_index, (images, labels) in enumerate(self.train_load):
                images, labels = images.to('cuda'), labels.to('cuda')

                model.zero_grad()
                log_probs = model(images)
                loss = criterion(log_probs, labels)
                loss.backward()
                optimizer.step()
                batch_loss.append(loss.item())
                if batch_index == 5:
                    break
        print('After Local Epoch : {}  \tLoss: {:.6f}'.format(iter, sum(batch_loss) / len(batch_loss)))

        self.weight = model.state_dict()
        return "Finish"

def select_model(args):
    if args['dataset'] == 'mnist':
        global_model = CNNMnist(args=args)
    elif args['dataset'] == 'cifar':
        global_model = CNNCifar(args=args)
    elif args['dataset'] == 'fmnist':
        global_model = CNNFashion_Mnist(args=args)
    return global_model
