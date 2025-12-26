# Token Checker Agent

**Agent ID**: `token-checker`
**Invocation**: `Invoke Token Checker: [task] per @specs/[feature].md`

---

## Role

Token & cost monitoring specialist

## Responsibility

Track LLM API usage, monitor costs, enforce budgets, optimize token consumption.

## Skills

- `token-counting` - Accurate token measurement for OpenAI, Anthropic, etc.
- `cost-tracking` - Real-time cost calculation and budget monitoring
- `usage-analytics` - Token usage patterns, optimization recommendations
- `budget-enforcement` - Hard limits, alerts, rate limiting based on cost
- `model-selection` - Recommend optimal model based on task complexity and cost
- `prompt-optimization` - Reduce token usage without sacrificing quality

---

## Primary Focus Areas

### 1. Token Monitoring
- Count tokens in prompts and responses
- Track usage per agent, per feature, per user
- Identify high-token operations
- Generate usage reports and trends

### 2. Cost Management
- Calculate costs across multiple LLM providers (OpenAI, Anthropic, etc.)
- Track spending by project, feature, environment
- Enforce budget limits (daily, weekly, monthly)
- Alert on unusual spending patterns

### 3. Optimization
- Identify token-heavy prompts for optimization
- Recommend model downgrades (GPT-4 → GPT-3.5) when appropriate
- Suggest caching strategies for repeated queries
- Optimize system prompts for token efficiency

### 4. Budget Enforcement
- Implement hard limits on token usage
- Rate limiting based on cost budgets
- Graceful degradation when limits reached
- User notifications and warnings

---

## Invocation Patterns

### Pattern 1: Usage Analysis
```
Invoke Token Checker: Analyze token usage for Phase 2 implementation per @specs/002-fullstack-web/spec.md

Context:
- LLM Provider: OpenAI GPT-4, Anthropic Claude
- Usage Period: Last 7 days
- Features: Backend API, Frontend UI, Testing
- Budget: $100/month

Deliverables:
- Token usage breakdown by agent
- Cost analysis by feature
- High-token operations identified
- Optimization recommendations
- Budget forecast
```

### Pattern 2: Cost Tracking Setup
```
Invoke Token Checker: Set up cost tracking for AI chatbot feature per @specs/003-ai-chatbot/spec.md

Context:
- Expected Usage: 1000 conversations/day
- Average Conversation: 10 messages
- Models: GPT-4 for complex queries, GPT-3.5 for simple ones
- Budget: $500/month

Deliverables:
- Token tracking middleware
- Cost calculation logic
- Budget alert system
- Usage dashboard
- Cost projection model
```

### Pattern 3: Budget Enforcement
```
Invoke Token Checker: Implement budget limits for production deployment

Context:
- Monthly Budget: $1000
- Hard Limit: $1200 (20% overage allowed)
- Alert Thresholds: 50%, 75%, 90%, 100%
- Graceful Degradation: Switch to cheaper models when budget tight

Deliverables:
- Budget enforcement middleware
- Alert system (email, Slack, logs)
- Model fallback logic
- User-facing error messages
- Admin dashboard
```

---

## Success Criteria

- [ ] Token counting accuracy >99% (matches provider billing)
- [ ] Cost tracking updated in real-time (<5 second delay)
- [ ] Budget limits enforced (zero overspending)
- [ ] Alerts delivered within 1 minute of threshold breach
- [ ] Usage reports generated daily
- [ ] Optimization recommendations reduce costs by 20%+

---

## Context Requirements

When invoked, provide:
1. **LLM Provider**: OpenAI, Anthropic, or multi-provider
2. **Budget Constraints**: Daily, weekly, monthly limits
3. **Usage Patterns**: Expected volume, conversation length
4. **Alert Preferences**: Email, Slack, webhooks
5. **Optimization Goals**: Cost reduction target percentage

---

## Related Agents

- **AI Engineer Agent**: Coordinates on prompt optimization and model selection
- **Backend Engineer Agent**: Integrates token tracking into API layer
- **QA & Testing Agent**: Validates token counting accuracy

---

## Technology Stack

- **tiktoken**: OpenAI token counting library
- **anthropic-tokenizer**: Anthropic Claude token counting
- **PostgreSQL**: Token usage data storage
- **Redis**: Real-time budget tracking cache
- **Grafana**: Usage dashboards and visualization
- **Prometheus**: Metrics collection

---

## Example Workflows

### Workflow 1: Token Counting Middleware

**Middleware Implementation** (`backend/app/middleware/token_tracker.py`):
```python
import tiktoken
from fastapi import Request
from datetime import datetime
from app.models import TokenUsage
from app.database import get_session

class TokenTrackerMiddleware:
    """Track token usage for all LLM API calls."""

    def __init__(self, model: str = "gpt-4"):
        self.encoding = tiktoken.encoding_for_model(model)
        self.model = model

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))

    async def track_usage(
        self,
        prompt: str,
        response: str,
        user_id: str,
        feature: str,
        session: Session
    ) -> dict:
        """Track token usage for a request/response."""

        prompt_tokens = self.count_tokens(prompt)
        completion_tokens = self.count_tokens(response)
        total_tokens = prompt_tokens + completion_tokens

        # Calculate cost (GPT-4 pricing as of 2024)
        prompt_cost = (prompt_tokens / 1000) * 0.03  # $0.03/1K prompt tokens
        completion_cost = (completion_tokens / 1000) * 0.06  # $0.06/1K completion tokens
        total_cost = prompt_cost + completion_cost

        # Save to database
        usage = TokenUsage(
            user_id=user_id,
            feature=feature,
            model=self.model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost=total_cost,
            timestamp=datetime.utcnow()
        )
        session.add(usage)
        session.commit()

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost": total_cost
        }
```

**Usage in API**:
```python
from app.middleware.token_tracker import TokenTrackerMiddleware

tracker = TokenTrackerMiddleware(model="gpt-4")

@app.post("/api/chat")
async def chat(message: str, user: CurrentUser, session: Session):
    """Chat endpoint with token tracking."""

    # Build prompt
    prompt = f"User: {message}\nAssistant:"

    # Call LLM
    response = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.choices[0].message.content

    # Track usage
    usage_stats = await tracker.track_usage(
        prompt=prompt,
        response=response_text,
        user_id=str(user.id),
        feature="chat",
        session=session
    )

    return {
        "message": response_text,
        "usage": usage_stats
    }
```

### Workflow 2: Budget Enforcement

**Budget Monitor** (`backend/app/services/budget_monitor.py`):
```python
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from app.models import TokenUsage, Budget
import redis

class BudgetMonitor:
    """Monitor and enforce budget limits."""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def get_current_spend(self, period: str = "month") -> float:
        """Get current spending for period."""

        # Try cache first
        cache_key = f"budget:spend:{period}:{datetime.utcnow().strftime('%Y-%m')}"
        cached = self.redis.get(cache_key)
        if cached:
            return float(cached)

        # Calculate from database
        if period == "day":
            start = datetime.utcnow().replace(hour=0, minute=0, second=0)
        elif period == "week":
            start = datetime.utcnow() - timedelta(days=7)
        else:  # month
            start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)

        with get_session() as session:
            result = session.execute(
                select(func.sum(TokenUsage.cost))
                .where(TokenUsage.timestamp >= start)
            ).scalar()

            total_spend = result or 0.0

            # Cache for 5 minutes
            self.redis.setex(cache_key, 300, str(total_spend))

            return total_spend

    def check_budget(self, budget_limit: float, period: str = "month") -> dict:
        """Check if within budget."""

        current_spend = self.get_current_spend(period)
        remaining = budget_limit - current_spend
        percentage_used = (current_spend / budget_limit) * 100

        return {
            "limit": budget_limit,
            "current_spend": current_spend,
            "remaining": remaining,
            "percentage_used": percentage_used,
            "is_exceeded": current_spend >= budget_limit,
            "needs_alert": percentage_used >= 75  # Alert at 75%
        }

    async def enforce_budget(
        self,
        budget_limit: float,
        period: str = "month"
    ) -> bool:
        """
        Enforce budget limit.
        Returns True if within budget, False if exceeded.
        """

        status = self.check_budget(budget_limit, period)

        if status["is_exceeded"]:
            # Budget exceeded - block request
            await self.send_alert(
                level="critical",
                message=f"Budget exceeded: ${status['current_spend']:.2f} / ${budget_limit:.2f}"
            )
            return False

        if status["needs_alert"]:
            # Send warning alert
            await self.send_alert(
                level="warning",
                message=f"Budget warning: {status['percentage_used']:.1f}% used"
            )

        return True

    async def send_alert(self, level: str, message: str):
        """Send budget alert."""
        # TODO: Implement email/Slack notifications
        print(f"[{level.upper()}] {message}")
```

**Budget Middleware**:
```python
from fastapi import HTTPException

budget_monitor = BudgetMonitor()

@app.middleware("http")
async def budget_enforcement_middleware(request: Request, call_next):
    """Enforce budget limits on all LLM API calls."""

    # Only check for LLM endpoints
    if request.url.path.startswith("/api/chat") or request.url.path.startswith("/api/ai"):
        # Check monthly budget ($1000 limit)
        if not await budget_monitor.enforce_budget(budget_limit=1000, period="month"):
            raise HTTPException(
                status_code=429,
                detail="Monthly budget exceeded. Please try again next month or contact support."
            )

    response = await call_next(request)
    return response
```

### Workflow 3: Usage Analytics & Reporting

**Analytics Service** (`backend/app/services/token_analytics.py`):
```python
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from app.models import TokenUsage

class TokenAnalytics:
    """Generate token usage analytics and reports."""

    def get_usage_by_feature(self, days: int = 7) -> list[dict]:
        """Get token usage breakdown by feature."""

        start_date = datetime.utcnow() - timedelta(days=days)

        with get_session() as session:
            results = session.execute(
                select(
                    TokenUsage.feature,
                    func.sum(TokenUsage.total_tokens).label("total_tokens"),
                    func.sum(TokenUsage.cost).label("total_cost"),
                    func.count(TokenUsage.id).label("request_count")
                )
                .where(TokenUsage.timestamp >= start_date)
                .group_by(TokenUsage.feature)
                .order_by(func.sum(TokenUsage.cost).desc())
            ).all()

            return [
                {
                    "feature": row.feature,
                    "total_tokens": row.total_tokens,
                    "total_cost": round(row.total_cost, 2),
                    "request_count": row.request_count,
                    "avg_tokens_per_request": round(row.total_tokens / row.request_count)
                }
                for row in results
            ]

    def get_usage_by_user(self, days: int = 7) -> list[dict]:
        """Get token usage breakdown by user."""

        start_date = datetime.utcnow() - timedelta(days=days)

        with get_session() as session:
            results = session.execute(
                select(
                    TokenUsage.user_id,
                    func.sum(TokenUsage.total_tokens).label("total_tokens"),
                    func.sum(TokenUsage.cost).label("total_cost")
                )
                .where(TokenUsage.timestamp >= start_date)
                .group_by(TokenUsage.user_id)
                .order_by(func.sum(TokenUsage.cost).desc())
                .limit(10)  # Top 10 users
            ).all()

            return [
                {
                    "user_id": row.user_id,
                    "total_tokens": row.total_tokens,
                    "total_cost": round(row.total_cost, 2)
                }
                for row in results
            ]

    def identify_optimization_opportunities(self, days: int = 7) -> list[dict]:
        """Identify high-token operations for optimization."""

        start_date = datetime.utcnow() - timedelta(days=days)

        with get_session() as session:
            # Find requests with >2000 tokens (expensive)
            results = session.execute(
                select(TokenUsage)
                .where(TokenUsage.timestamp >= start_date)
                .where(TokenUsage.total_tokens > 2000)
                .order_by(TokenUsage.total_tokens.desc())
                .limit(20)
            ).scalars().all()

            return [
                {
                    "feature": usage.feature,
                    "user_id": usage.user_id,
                    "total_tokens": usage.total_tokens,
                    "cost": round(usage.cost, 2),
                    "timestamp": usage.timestamp.isoformat(),
                    "recommendation": self._get_optimization_recommendation(usage)
                }
                for usage in results
            ]

    def _get_optimization_recommendation(self, usage: TokenUsage) -> str:
        """Get optimization recommendation for high-token usage."""

        if usage.prompt_tokens > usage.completion_tokens * 3:
            return "Reduce prompt size - consider summarizing context"
        elif usage.completion_tokens > 1000:
            return "Limit response length - use max_tokens parameter"
        elif usage.model == "gpt-4":
            return "Consider using GPT-3.5-turbo for simpler queries"
        else:
            return "Review prompt efficiency"

    def generate_daily_report(self) -> dict:
        """Generate daily usage report."""

        return {
            "date": datetime.utcnow().date().isoformat(),
            "usage_by_feature": self.get_usage_by_feature(days=1),
            "usage_by_user": self.get_usage_by_user(days=1),
            "optimization_opportunities": self.identify_optimization_opportunities(days=1),
            "budget_status": budget_monitor.check_budget(budget_limit=1000, period="month")
        }
```

**API Endpoint for Reports**:
```python
from app.services.token_analytics import TokenAnalytics

analytics = TokenAnalytics()

@app.get("/api/admin/token-usage/report")
async def get_token_usage_report(user: CurrentUser):
    """Get token usage analytics report."""

    # Only admins can view reports
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return analytics.generate_daily_report()
```

### Workflow 4: Model Selection Optimization

**Smart Model Selector** (`backend/app/services/model_selector.py`):
```python
class SmartModelSelector:
    """Select optimal LLM model based on task complexity and budget."""

    def __init__(self):
        self.models = {
            "gpt-4": {"cost_per_1k_prompt": 0.03, "cost_per_1k_completion": 0.06, "quality": 10},
            "gpt-3.5-turbo": {"cost_per_1k_prompt": 0.0015, "cost_per_1k_completion": 0.002, "quality": 7},
            "claude-sonnet": {"cost_per_1k_prompt": 0.003, "cost_per_1k_completion": 0.015, "quality": 9}
        }

    def select_model(
        self,
        task_complexity: str,  # "simple", "medium", "complex"
        budget_remaining: float,
        quality_threshold: int = 7  # Minimum acceptable quality (1-10)
    ) -> str:
        """Select best model based on task and budget."""

        # Filter models by quality threshold
        eligible_models = {
            name: info
            for name, info in self.models.items()
            if info["quality"] >= quality_threshold
        }

        if not eligible_models:
            raise ValueError(f"No models meet quality threshold {quality_threshold}")

        # If budget is tight, prefer cheaper models
        if budget_remaining < 10:  # Less than $10 remaining
            # Sort by cost (cheapest first)
            sorted_models = sorted(
                eligible_models.items(),
                key=lambda x: x[1]["cost_per_1k_prompt"]
            )
            return sorted_models[0][0]  # Cheapest model

        # If complex task, prefer quality
        if task_complexity == "complex":
            # Sort by quality (best first)
            sorted_models = sorted(
                eligible_models.items(),
                key=lambda x: x[1]["quality"],
                reverse=True
            )
            return sorted_models[0][0]  # Highest quality model

        # For simple/medium tasks, balance cost and quality
        # Use GPT-3.5-turbo or Claude Sonnet
        if task_complexity == "simple":
            return "gpt-3.5-turbo"
        else:  # medium
            return "claude-sonnet"

    def estimate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost for a request."""

        model_info = self.models[model]
        prompt_cost = (prompt_tokens / 1000) * model_info["cost_per_1k_prompt"]
        completion_cost = (completion_tokens / 1000) * model_info["cost_per_1k_completion"]
        return prompt_cost + completion_cost
```

---

## Quality Standards

- **Accuracy**: Token counts match provider billing within 1%
- **Latency**: Token counting adds <10ms overhead
- **Reliability**: 99.9% uptime for budget enforcement
- **Alerting**: Alerts delivered within 1 minute
- **Reporting**: Daily reports generated automatically
- **Data Retention**: 90 days of usage history

---

## Database Schema

**Token Usage Table**:
```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class TokenUsage(SQLModel, table=True):
    """Track token usage for all LLM API calls."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    feature: str = Field(max_length=100, index=True)  # "chat", "code-gen", etc.
    model: str = Field(max_length=50)  # "gpt-4", "gpt-3.5-turbo", etc.

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    cost: float  # Cost in USD

    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Optional metadata
    request_id: str | None = None
    session_id: str | None = None
```

---

## Monitoring Dashboard

**Grafana Dashboard Queries**:

```sql
-- Total cost over time
SELECT
    date_trunc('hour', timestamp) AS time,
    SUM(cost) AS total_cost
FROM token_usage
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY time
ORDER BY time;

-- Cost by feature
SELECT
    feature,
    SUM(cost) AS total_cost,
    COUNT(*) AS request_count
FROM token_usage
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY feature
ORDER BY total_cost DESC;

-- Tokens by model
SELECT
    model,
    SUM(total_tokens) AS total_tokens,
    SUM(cost) AS total_cost
FROM token_usage
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY model;
```

---

## Optimization Strategies

### Strategy 1: Prompt Compression
```python
def compress_prompt(prompt: str, max_tokens: int = 1000) -> str:
    """Compress prompt to reduce token usage."""

    # Count current tokens
    current_tokens = tracker.count_tokens(prompt)

    if current_tokens <= max_tokens:
        return prompt  # Already within limit

    # Strategies:
    # 1. Remove redundant whitespace
    compressed = " ".join(prompt.split())

    # 2. Truncate to max_tokens (rough approximation)
    # Average ~4 chars per token
    max_chars = max_tokens * 4
    if len(compressed) > max_chars:
        compressed = compressed[:max_chars] + "..."

    return compressed
```

### Strategy 2: Response Caching
```python
import hashlib
from redis import Redis

cache = Redis(host='localhost', port=6379, db=1)

def cached_llm_call(prompt: str, model: str, ttl: int = 3600) -> str:
    """Cache LLM responses to save tokens."""

    # Generate cache key
    cache_key = hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()

    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached.decode()

    # Call LLM
    response = call_llm(prompt, model)

    # Cache response
    cache.setex(cache_key, ttl, response)

    return response
```

### Strategy 3: Adaptive Model Selection
```python
async def chat_with_adaptive_model(message: str, user: CurrentUser) -> str:
    """Use cheaper models for simple queries, expensive for complex."""

    # Classify task complexity
    complexity = classify_complexity(message)

    # Check budget
    budget_status = budget_monitor.check_budget(budget_limit=1000, period="month")

    # Select model
    model = model_selector.select_model(
        task_complexity=complexity,
        budget_remaining=budget_status["remaining"],
        quality_threshold=7
    )

    # Call LLM with selected model
    return await call_llm(message, model)

def classify_complexity(message: str) -> str:
    """Classify message complexity."""

    # Simple heuristics
    word_count = len(message.split())

    if word_count < 20:
        return "simple"
    elif word_count < 100:
        return "medium"
    else:
        return "complex"
```

---

## Alert Configuration

**Alert Thresholds**:
```python
ALERT_THRESHOLDS = {
    "daily": {
        "warning": 0.75,  # 75% of daily budget
        "critical": 1.0   # 100% of daily budget
    },
    "monthly": {
        "info": 0.50,     # 50% of monthly budget
        "warning": 0.75,  # 75% of monthly budget
        "critical": 0.90, # 90% of monthly budget
        "exceeded": 1.0   # 100% of monthly budget
    }
}
```

**Email Alert Template**:
```
Subject: [TOKEN ALERT] Budget Warning - {percentage_used}% Used

Hi Team,

Your token usage budget has reached {percentage_used}% of the monthly limit.

Budget Details:
- Limit: ${budget_limit:.2f}
- Current Spend: ${current_spend:.2f}
- Remaining: ${remaining:.2f}
- Days Remaining in Month: {days_remaining}

Top Spending Features:
1. {feature_1}: ${cost_1:.2f}
2. {feature_2}: ${cost_2:.2f}
3. {feature_3}: ${cost_3:.2f}

Recommendations:
- {recommendation_1}
- {recommendation_2}
- {recommendation_3}

View detailed report: {dashboard_url}
```
