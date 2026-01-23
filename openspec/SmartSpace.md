# SmartSpace User Guide

**Your Complete Guide to SmartSpace - The Autonomous Pay-Per-Use API Gateway**

---

## What is SmartSpace?

SmartSpace is an autonomous pay-per-use API access gateway that enables secure AI model usage with USDC payments on the Arc blockchain. Think of it as your unified access point to multiple AI models - from OpenAI and Anthropic to local models like Qalb (Urdu LLM) and DeepSeek.

### Key Benefits

✅ **No API Key Management** - You never need to manage or expose API keys  
✅ **Pay-As-You-Go** - Single USDC transaction per request, no subscriptions  
✅ **Unified Access** - One API key for all models, just change the endpoint  
✅ **No Middleman Charges** - Direct pay-as-you-go pricing, transparent costs  
✅ **Model Flexibility** - Easy switching between models via dropdown  
✅ **Full Transparency** - Complete audit trail for every request and payment  
✅ **Autonomous Control** - Set budgets, policies, and spending limits  

---

## Getting Started

### Step 1: Create Your Account

1. Visit the SmartSpace landing page
2. Click "Sign Up" to create your account
3. Provide your email and create a password
4. Verify your email address

### Step 2: Add USDC to Your Account

1. Navigate to the Billing section in your dashboard
2. Click "Add Funds" or "Deposit USDC"
3. Connect your Arc blockchain wallet
4. Transfer USDC to your SmartSpace account (Arc testnet for demo)
5. Your balance will be credited automatically

**Note**: For the hackathon demo, we use Arc testnet. Make sure you have testnet USDC in your wallet.

### Step 3: Get Your API Key

1. Once your account is set up and funded, go to Dashboard
2. Navigate to "API Keys" section
3. Click "Generate API Key"
4. Copy and securely store your API key
5. **Important**: This single API key works for all models!

### Step 4: Select Your Model

1. In the Dashboard, use the model dropdown to select your preferred model:
   - **Qalb (Urdu LLM)** - For Urdu language tasks
   - **DeepSeek R1** - Advanced reasoning model
   - **LLaMA-2** - General purpose model
   - Additional models as available

2. The system will automatically route your requests to the selected model

### Step 5: Make Your First API Call

1. Go to the "API Call Interface" in your Dashboard
2. Select your model from the dropdown
3. Enter your prompt or request
4. Optionally set max tokens
5. Click "Execute Request (Pay with USDC)"
6. Review the estimated cost before confirming
7. Your request will be processed and you'll receive the response

---

## Core Features

### 1. Unified API Access

**One API Key, All Models**

SmartSpace provides a single API key that works across all supported models. You don't need separate keys for each provider. Simply change the endpoint or model name in your request to switch between models.

**Example:**
```javascript
// Same API key, different models
POST /api/v1/requests
Headers: { "Authorization": "Bearer YOUR_API_KEY" }
Body: {
  "model": "qalb-urdu",
  "prompt": "Your request here"
}

// Switch to DeepSeek - same API key!
Body: {
  "model": "deepseek-r1",
  "prompt": "Your request here"
}
```

### 2. Pay-Per-Use Model

**How It Works:**

1. **Cost Estimation**: Before executing your request, SmartSpace estimates the cost
2. **Payment Processing**: You pay the estimated amount in USDC (~500ms)
3. **API Execution**: The request is routed to your selected model
4. **Response Delivery**: You receive the response and a transaction receipt

**Key Points:**
- No monthly subscriptions
- Pay only for what you use
- Transparent pricing per request
- No hidden fees or middleman charges
- Transaction hash provided for every payment

### 3. Model Selection & Switching

**Available Models (Demo):**

- **Qalb (Urdu LLM)** - Specialized for Urdu language processing
  - Model ID: `qalb-urdu`
  - Best for: Urdu text generation, translation, analysis

- **DeepSeek R1** - Advanced reasoning and problem-solving
  - Model ID: `deepseek-r1`
  - Best for: Complex reasoning, code generation, analysis

- **LLaMA-2** - General purpose language model
  - Model ID: `llama2`
  - Best for: General text generation, Q&A, summarization

**How to Switch Models:**

1. **Via Dashboard**: Use the dropdown in the API Call Interface
2. **Via API**: Change the `model` parameter in your request
3. **Via Endpoint**: Different models may have different endpoint paths

**Note**: Model names must match exactly (case-sensitive). Check available models in your dashboard.

### 4. Budget Management

**Three-Level Budget System:**

1. **Per-Request Limit**: Maximum USDC per single request (default: $10.00)
2. **Daily Budget**: Maximum USDC per day (default: $100.00)
3. **Monthly Budget**: Maximum USDC per month (default: $3000.00)

**How Budgets Work:**

- All three levels must pass for request approval
- Budgets are checked in real-time
- Once a budget is exhausted, requests are blocked until reset
- You can adjust budgets in your Project Settings

**Setting Budgets:**

1. Go to Dashboard → Projects
2. Select your project
3. Navigate to "Budget Settings"
4. Adjust per-request, daily, or monthly limits
5. Save changes

### 5. Policy & Security

**Provider/Model Whitelisting:**

- You can only use providers and models you've explicitly approved
- Configure allowed providers in your Project Settings
- Configure allowed models per provider
- System policies cannot be overridden (security first)

**Rate Limiting:**

- Set requests per minute/hour/day
- Set token limits per hour
- Prevent unexpected spending spikes

**Risk Assessment:**

SmartSpace automatically assesses each request for:
- Cost spikes (>3x average)
- Rate spikes (unusual volume)
- Unusual provider/model usage
- Unusual time patterns
- Budget exhaustion patterns

**Risk-Based Routing:**

- **Low Risk (≤3)**: Auto-approved, fast processing (<100ms)
- **Medium Risk (3-7)**: Requires review, comprehensive analysis (<1s)
- **High Risk (>7)**: Automatically rejected for safety

### 6. Audit Trail

**Complete Transparency:**

Every request and payment is logged with:
- Request details (model, prompt, parameters)
- Cost estimation and actual cost
- Payment transaction hash
- Block number and confirmation
- Policy checks and decisions
- Risk assessment scores
- Response data and timing

**Accessing Audit Logs:**

1. Go to Dashboard → Usage
2. View "Recent Activity" for quick overview
3. Click on any request for detailed audit trail
4. Export logs for compliance/accounting

---

## Using the API

### Authentication

All API requests require your API key in the Authorization header:

```javascript
Authorization: Bearer YOUR_API_KEY
```

### Making a Request

**Endpoint:** `POST /api/v1/requests`

**Request Body:**
```json
{
  "model": "deepseek-r1",
  "prompt": "Explain quantum computing in simple terms",
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "request_id": "req_123456",
  "status": "executed",
  "response": "Quantum computing uses quantum mechanics...",
  "cost": 0.0023,
  "tx_hash": "0xabc123...",
  "tokens_used": 245,
  "latency_ms": 1234
}
```

### Model Switching via API

To switch models, simply change the `model` parameter:

```json
// Qalb (Urdu LLM)
{ "model": "qalb-urdu", "prompt": "آپ کیسے ہیں؟" }

// DeepSeek R1
{ "model": "deepseek-r1", "prompt": "Solve this math problem..." }

// LLaMA-2
{ "model": "llama2", "prompt": "Write a story about..." }
```

### Error Handling

**Common Error Codes:**

- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Invalid or missing API key
- `402 Payment Required` - Insufficient balance
- `403 Forbidden` - Model/provider not in whitelist
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server-side error

**Error Response Format:**
```json
{
  "error": "Insufficient funds",
  "error_code": "INSUFFICIENT_BALANCE",
  "required_amount": 0.05,
  "available_balance": 0.02
}
```

---

## Payment & Billing

### How Payments Work

1. **Cost Estimation**: System estimates cost based on:
   - Selected model
   - Estimated input/output tokens
   - Current provider pricing

2. **Payment Execution**: 
   - USDC transaction on Arc blockchain (~500ms)
   - Transaction hash returned immediately
   - Payment must complete before API call

3. **Cost Variance Tracking**:
   - Estimated vs actual cost logged
   - No refunds for over-estimation (avoids gas fees)
   - Variance data used to improve estimates

### Viewing Transactions

1. Go to Dashboard → Billing
2. View "Transaction History"
3. Each transaction shows:
   - Amount paid (USDC)
   - Transaction hash
   - Block number
   - Request details
   - Model used

### Adding Funds

1. Go to Dashboard → Billing
2. Click "Add Funds"
3. Connect your Arc wallet
4. Enter amount to deposit
5. Confirm transaction
6. Balance updates automatically

### Understanding Costs

**Cost Factors:**
- Model selection (different models have different rates)
- Input tokens (your prompt length)
- Output tokens (response length)
- Provider pricing (may vary)

**Cost Calculation:**
```
Total Cost = (Input Tokens / 1000 × Input Rate) + (Output Tokens / 1000 × Output Rate)
```

**Example:**
- Model: DeepSeek R1
- Input: 100 tokens @ $0.001/1k = $0.0001
- Output: 200 tokens @ $0.002/1k = $0.0004
- **Total: $0.0005 USDC**

---

## Best Practices

### 1. Budget Management

✅ **Do:**
- Set realistic budgets based on expected usage
- Monitor spending regularly
- Use per-request limits to prevent expensive mistakes
- Review daily/monthly spending patterns

❌ **Don't:**
- Set budgets too high without monitoring
- Ignore budget warnings
- Disable all budget limits

### 2. Model Selection

✅ **Do:**
- Choose the right model for your task:
  - **Qalb** for Urdu language tasks
  - **DeepSeek R1** for complex reasoning
  - **LLaMA-2** for general purposes
- Test different models for your use case
- Monitor costs per model

❌ **Don't:**
- Use expensive models for simple tasks
- Switch models unnecessarily (adds overhead)
- Ignore model-specific capabilities

### 3. API Usage

✅ **Do:**
- Store your API key securely (environment variables)
- Use appropriate max_tokens limits
- Handle errors gracefully
- Monitor request latency and costs
- Keep audit logs for compliance

❌ **Don't:**
- Commit API keys to version control
- Make unnecessary requests
- Ignore rate limits
- Skip error handling

### 4. Security

✅ **Do:**
- Keep your API key secret
- Use HTTPS for all API calls
- Regularly review audit logs
- Monitor for unusual activity
- Set up provider/model whitelists

❌ **Don't:**
- Share API keys
- Use API keys in client-side code
- Disable security policies
- Ignore risk warnings

---

## Troubleshooting

### Common Issues

#### Issue: "Insufficient Funds"

**Problem:** Your account balance is too low for the request.

**Solution:**
1. Check your current balance in Dashboard → Billing
2. Add more USDC to your account
3. Verify the transaction completed
4. Try your request again

#### Issue: "Model Not in Whitelist"

**Problem:** The model you're trying to use isn't approved for your project.

**Solution:**
1. Go to Dashboard → Projects → Settings
2. Navigate to "Allowed Models"
3. Add the model to your whitelist
4. Save changes
5. Try your request again

#### Issue: "Budget Exceeded"

**Problem:** One of your budget limits (per-request, daily, or monthly) has been exceeded.

**Solution:**
1. Check which budget limit was hit in Dashboard → Usage
2. Either:
   - Wait for the period to reset (daily/monthly)
   - Increase the budget limit in Project Settings
   - Reduce request size/cost

#### Issue: "Request Rejected - High Risk"

**Problem:** The system detected unusual activity and rejected the request for safety.

**Solution:**
1. Review the risk assessment details in the audit log
2. Check if this is expected behavior
3. If legitimate, contact support
4. Consider adjusting your usage patterns

#### Issue: "Payment Failed"

**Problem:** The USDC transaction failed on the blockchain.

**Solution:**
1. Check your Arc wallet has sufficient USDC
2. Verify network connectivity
3. Check Arc testnet status
4. Retry the request
5. If persistent, contact support with transaction hash

#### Issue: "Model Not Available"

**Problem:** The selected model isn't available or running.

**Solution:**
1. Check model status in Dashboard
2. Try a different model
3. Verify Ollama is running (for local models)
4. Check model name spelling (case-sensitive)

---

## Frequently Asked Questions (FAQ)

### General Questions

**Q: What is SmartSpace?**  
A: SmartSpace is a pay-per-use API gateway that lets you access multiple AI models with a single API key, paying only for what you use with USDC.

**Q: Do I need separate API keys for each model?**  
A: No! SmartSpace provides one API key that works for all models. Just change the model parameter in your request.

**Q: How do I switch between models?**  
A: Use the dropdown in the Dashboard, or change the `model` parameter in your API request. No need to change API keys!

**Q: What blockchain does SmartSpace use?**  
A: SmartSpace uses the Arc blockchain with USDC (USD Coin) stablecoin for payments.

**Q: Is SmartSpace secure?**  
A: Yes! SmartSpace never exposes your API keys, uses blockchain for transparent payments, and provides complete audit trails.

### Payment Questions

**Q: How do I add funds to my account?**  
A: Go to Dashboard → Billing → Add Funds, connect your Arc wallet, and transfer USDC.

**Q: How much does each request cost?**  
A: Costs vary by model and token usage. You'll see an estimated cost before confirming each request.

**Q: Can I get a refund if I overpay?**  
A: SmartSpace uses estimated costs to avoid multiple transactions. Over-estimation is logged but not refunded (to save gas fees). Under-estimation is also tracked.

**Q: What happens if my payment fails?**  
A: The request won't be executed. Check your balance and Arc wallet connection, then retry.

**Q: How fast are payments?**  
A: USDC payments on Arc typically complete in ~500ms.

### Model Questions

**Q: What models are available?**  
A: For the demo: Qalb (Urdu LLM), DeepSeek R1, and LLaMA-2. More models will be added.

**Q: How do I know which model to use?**  
A: 
- **Qalb**: Urdu language tasks
- **DeepSeek R1**: Complex reasoning, code, analysis
- **LLaMA-2**: General text generation, Q&A

**Q: Can I use multiple models in one request?**  
A: No, each request uses one model. You can make multiple requests with different models.

**Q: Are models always available?**  
A: Local models (Ollama) require the Ollama service to be running. Check model status in your dashboard.

### Technical Questions

**Q: What's the API rate limit?**  
A: Rate limits are configurable per project. Default limits are shown in your Project Settings.

**Q: How do I handle errors?**  
A: Check the error code and message in the API response. Common solutions are in the Troubleshooting section.

**Q: Can I see my request history?**  
A: Yes! Go to Dashboard → Usage → Recent Activity to see all your requests and payments.

**Q: How do I export my audit logs?**  
A: Go to Dashboard → Usage, select the time range, and click "Export Logs" for compliance/accounting.

**Q: What data is stored?**  
A: SmartSpace stores request metadata, costs, transaction hashes, and audit trails. Your prompt content may be logged for service improvement (check privacy policy).

---

## Support & Resources

### Getting Help

- **Chatbot**: Use the Gemini chatbot on the landing page or dashboard for instant help
- **Documentation**: This guide (SmartSpace.md) is your comprehensive resource
- **Dashboard**: Check your Dashboard for usage stats, budgets, and settings
- **Audit Logs**: Review audit logs for detailed request information

### Key Resources

- **Dashboard**: Your main control center
- **Billing**: Manage payments and view transactions
- **Usage**: View activity and export logs
- **Projects**: Configure budgets, policies, and model whitelists
- **API Keys**: Manage your API keys

### Contact

For additional support or questions not covered in this guide:
- Use the chatbot for immediate assistance
- Check the Troubleshooting section
- Review your audit logs for request details

---

## Quick Reference

### Dashboard Navigation

- **Home**: Overview and quick stats
- **Projects**: Manage projects, budgets, and policies
- **Usage**: View activity and audit logs
- **Billing**: Manage payments and view transactions
- **Settings**: Account and API key management

### API Quick Start

```bash
# Set your API key
export SMARTSPACE_API_KEY="your_api_key_here"

# Make a request
curl -X POST https://api.smartspace.com/v1/requests \
  -H "Authorization: Bearer $SMARTSPACE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1",
    "prompt": "Hello, world!",
    "max_tokens": 100
  }'
```

### Model IDs

- `qalb-urdu` - Qalb (Urdu LLM)
- `deepseek-r1` - DeepSeek R1
- `llama2` - LLaMA-2

### Default Budgets

- Per-Request: $10.00 USDC
- Daily: $100.00 USDC
- Monthly: $3000.00 USDC

---

**Last Updated**: 2026-01-13  
**Version**: 1.0 (Hackathon Demo)

---

*This guide is designed to help you get the most out of SmartSpace. The Gemini chatbot can answer questions based on this documentation. For the most up-to-date information, always check your Dashboard.*

