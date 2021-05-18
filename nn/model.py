import torch
import torch.nn as nn


class NNRegressor(nn.Module):
    def __init__(
            self,
            embed_dim=10,
            n_store=46,
            n_department=100,
            n_type=3,
            n_feat=21,
            hidden_dim1=100,
            hidden_dim2=50
    ):
        super(NNRegressor, self).__init__()
        self.store_embedding = nn.Embedding(num_embeddings=n_store, embedding_dim=embed_dim)
        self.dept_embedding = nn.Embedding(num_embeddings=n_department, embedding_dim=embed_dim)
        self.type_embedding = nn.Embedding(num_embeddings=n_type, embedding_dim=embed_dim)
        self.linear1 = nn.Linear(in_features=embed_dim*3 + n_feat, out_features=hidden_dim1)
        self.drop1 = nn.Dropout(0.3)
        self.linear2 = nn.Linear(in_features=hidden_dim1, out_features=hidden_dim2)
        self.drop2 = nn.Dropout(0.3)
        self.linear_out = nn.Linear(in_features=hidden_dim2, out_features=1)

    def init_weight(self):
        torch.nn.init.xavier_normal(self.linear1.weight)
        torch.nn.init.xavier_normal(self.linear2.weight)
        torch.nn.init.xavier_normal(self.linear_out.weight)

    def forward(self, inputs):
        store_embed = self.store_embedding(inputs['store_id'])
        try:
            dept_embed = self.dept_embedding(inputs['dept_id'])
        except:
            print(inputs['dept_id'].shape)
            raise IndexError(f"{inputs['dept_id']}")

        type_embed = self.type_embedding(inputs['store_type'])
        markdown_f = inputs['markdown_f']
        feature_f = inputs['feature_f']
        inputs = torch.cat([store_embed, dept_embed, type_embed, markdown_f, feature_f], dim=-1)
        out = nn.ReLU()(self.linear1(inputs))
        out = self.drop1(out)
        out = nn.ReLU()(self.linear2(out))
        out = self.drop2(out)
        out = self.linear_out(out)
        return out
