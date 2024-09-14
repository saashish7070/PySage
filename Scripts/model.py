#model made and used as a scratch training - khagendra karki
import math
import torch
import torch.nn as nn
from transformers import PreTrainedModel, PretrainedConfig

# standard value #######
vocab_size=20256
batch_size=1
seq_len=10
d_model=1024
n_layers=12
d_ff=2732
n_heads=16
######################

class ModelConfig(PretrainedConfig):
    def __init__(self, vocab_size=20256, d_model=1024, n_layers=12, d_ff=2732, n_heads=16, **kwargs):
        super().__init__(**kwargs)
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.n_layers = n_layers
        self.d_ff = d_ff
        self.n_heads = n_heads

class LinearScalingRotaryEmbedding(nn.Module):
  def __init__(self, dim, base=10000): # dim -> head_size
    super().__init__()
    inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim)) # (dim // 2)
    self.register_buffer('inv_freq', inv_freq)
    self.seq_len_cached = None # seq_len
    self.cos_cached = None
    self.sin_cached = None


  def forward(self, x, seq_dim = -2): # x -> (batch_size, num_heads, seq_len, head_size)
    seq_len = x.shape[seq_dim] # seq_len
    if seq_len != self.seq_len_cached:
        self.seq_len_cached = seq_len
        t = torch.arange(x.shape[seq_dim], device=x.device, dtype=self.inv_freq.dtype) # (seq_len)
        freqs = torch.einsum('i,j->ij', t, self.inv_freq) # ( seq_len, head_size // 2)
        # print("The dimension of freqs is ", freqs.shape)
        emb = torch.cat((freqs, freqs), dim=-1).to(x.device) # ( seq_len, head_size )
        self.cos_cached = emb.cos()# (seq_len, head_size)
        # print("The dimension of cos embedding is", self.cos_cached.shape)
        self.sin_cached = emb.sin() # (seq_len, head_size)

    return self.cos_cached, self.sin_cached

  def apply_rotary_pos_emb(self, q, k, sin, cos): # q -> (batch_size, num_heads, seq_len, head_size)
    # apply rotary embeddings to q and k
    q  = (q * cos) + (self.rotate_half(q) * sin) # ( batch_size, num_heads, seq_len, head_size)
    k  = (k * cos) + (self.rotate_half(k) * sin) # (batch_size, num_heads, seq_len, head_size)

    return q, k

  def rotate_half(self, x): # x -> (batch_size, num_heads, seq_len, head_size)
    x1, x2 = x.chunk(2, dim=-1) # (batch_size, num_heads, seq_len, head_size // 2)
    return torch.cat((-x2, x1), dim=-1) # (batch_size, num_heads, seq_len, head_size)

class RMSNorm(nn.Module):
    def __init__(self, d_model, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(d_model))

    def forward(self, x):
        norm = x.norm(keepdim=True, dim=-1, p=2)  # RMS norm over last dimension
        return self.weight * (x / (norm + self.eps))

class SelfAttention(nn.Module):
  def __init__(self, config):
    super().__init__()
    self.num_attention_heads = config.n_heads # n_head
    self.attention_head_size = config.d_model // config.n_heads # head_size
    self.all_head_size = self.num_attention_heads * self.attention_head_size # d_model

    self.query = nn.Linear(config.d_model, self.all_head_size) # (d_model, d_model )
    self.key = nn.Linear(config.d_model, self.all_head_size) # (d_model, d_model)
    self.value = nn.Linear(config.d_model, self.all_head_size) # (d_model, d_model)

    self.out = nn.Linear(self.all_head_size, config.d_model) # (d_model, d_model)
    self.rotary_emb = LinearScalingRotaryEmbedding(self.attention_head_size)

  def transpose_for_scores(self, x): # x -> (batch_size, seq_len, d_model)
    new_x_shape = x.size()[:-1] + (self.num_attention_heads, self.attention_head_size) # (batch_size, seq_len, n_heads, head_size)
    x = x.view(*new_x_shape)
    return x.permute(0, 2, 1, 3) # (batch_size, n_heads, seq_len, head_size)

  def forward(self, hidden_states): # hidden_states -> (batch_size, seq_len, d_model)
    mixed_query_layer = self.query(hidden_states) # (batch_size, seq_len, d_model)
    mixed_key_layer = self.key(hidden_states) # (batch_size, seq_len, d_model)
    mixed_value_layer = self.value(hidden_states) # (batch_size, seq_len, d_model)

    query_layer = self.transpose_for_scores(mixed_query_layer) # (batch_size, n_heads, seq_len, head_size)
    key_layer = self.transpose_for_scores(mixed_key_layer) # (batch_size, n_heads, seq_len, head_size)
    value_layer = self.transpose_for_scores(mixed_value_layer) # (batch_size, n_heads, seq_len, head_size)

    # Apply rotary embeddings
    sin, cos = self.rotary_emb(query_layer) # (seq_len, head_size)
    query_layer, key_layer = self.rotary_emb.apply_rotary_pos_emb(query_layer, key_layer, sin, cos) # (batch_size, n_heads, seq_len, head_size)

    attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2)) # (batch_size, n_heads, seq_len, seq_len)
    attention_scores = attention_scores / math.sqrt(self.attention_head_size) # (batch_size, n_heads, seq_len, seq_len)
    attention_probs = nn.Softmax(dim=-1)(attention_scores) # (batch_size, n_heads, seq_len, seq_len)

    context_layer = torch.matmul(attention_probs, value_layer) # (batch_size, n_heads, seq_len, head_size)
    context_layer = context_layer.permute(0, 2, 1, 3).contiguous() # (batch_size, seq_len, n_heads, head_size)
    new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,) # (batch_size, seq_len, d_model)
    context_layer = context_layer.view(*new_context_layer_shape) # (batch_size, seq_len, d_model)
    attention_output = self.out(context_layer) # (batch_size, seq_len, d_model)
    return attention_output

class FeedForward(nn.Module):
  def __init__(self, config):
    super().__init__()
    self.gate_proj = nn.Linear(config.d_model, config.d_ff, bias=False)
    self.up_proj = nn.Linear(config.d_model, config.d_ff, bias=False)
    self.down_proj = nn.Linear(config.d_ff, config.d_model, bias=False)
    self.act_fn = nn.SiLU()

  def forward(self, x):
    gate_output = self.act_fn(self.gate_proj(x))
    up_output = self.up_proj(x)
    intermediate_output = gate_output * up_output
    return self.down_proj(intermediate_output)

class Layer(nn.Module):
  def __init__(self, config):
    super().__init__()
    self.attention = SelfAttention(config)
    self.feed_forward = FeedForward(config)
    self.norm = RMSNorm(config.d_model)


  def forward(self, hidden_states): # hidden_states -> (batch_size, seq_len, d_model)
    normed_hidden_states = self.norm(hidden_states)
    attention_output = self.attention(normed_hidden_states) # (batch_size, seq_len, d_model)
    hidden_states = self.norm(hidden_states + attention_output) # (batch_size, seq_len, d_model)
    feed_forward_output = self.feed_forward(hidden_states) # (batch_size, seq_len, d_model)

    return hidden_states + feed_forward_output # (batch_size, seq_len, d_model)

class Model(PreTrainedModel):
  def __init__(self, config):
    super().__init__(config)
    self.embedding = nn.Embedding(config.vocab_size, config.d_model) # (vocab_size, d_model)
    self.layers = nn.ModuleList([Layer(config) for _ in range(config.n_layers)])
    self.final_layer_norm = RMSNorm(config.d_model)
    self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False) # ( d_model, vocab_size)

  def forward(self, input_ids): # input_ids -> (batch_size, seq_len)
    hidden_states = self.embedding(input_ids) # (batch_size, seq_len, d_model)
    for layer in self.layers:
        hidden_states = layer(hidden_states) # (batch_size, seq_len, d_model)
    hidden_states = self.final_layer_norm(hidden_states) # (batch_size, seq_len, d_model)
    logits = self.lm_head(hidden_states) # (batch_size, seq_len, vocab_size)
    return logits

# Example usage


# config = ModelConfig()
# model = Model(config)
# input_ids = torch.randint(0, config.vocab_size, (3, 1024))  # Batch size of 1, sequence length of 10
# logits = model(input_ids)
# print(logits.shape)  # Should be (1, 10, config.vocab_size)
