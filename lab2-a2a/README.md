# AIOps-Enabled Agent2Agent Communication Framework for Automated ITIL Service Management

**Author:** Luis Rubio, BSCs

## Abstract

Artificial Intelligence for IT Operations (AIOps) represents a paradigm shift in IT service management, leveraging machine learning, natural language processing, and automated reasoning to enhance operational efficiency and reduce human intervention in routine IT tasks. AIOps platforms integrate diverse data sources, apply advanced analytics to identify patterns and anomalies, and provide intelligent insights for proactive incident management, performance optimization, and capacity planning. The convergence of AI technologies with traditional IT operations enables organizations to achieve higher service availability, faster incident resolution, and improved resource utilization through predictive analytics and automated decision-making processes. The evolution toward Agentic AIOps introduces autonomous intelligent agents that can independently execute complex IT operations tasks, make contextual decisions, and collaborate through standardized communication protocols to deliver comprehensive service management automation.

The integration of AIOps capabilities with ITIL v4 practices offers significant potential for automating core service management processes, including incident management, problem management, change management, and service request fulfillment. Through intelligent agent-based architectures, Agentic AIOps can automate ticket classification and routing, perform root cause analysis, orchestrate remediation workflows, and maintain comprehensive service catalogs. This automation reduces manual effort, minimizes human error, and enables IT teams to focus on strategic initiatives while ensuring consistent adherence to ITIL best practices through standardized, AI-driven processes that continuously learn and adapt to organizational patterns. The agentic approach enables autonomous decision-making and inter-agent collaboration, creating self-managing IT ecosystems that can respond to complex scenarios without human intervention.

## 1. Introduction

This research explores the application of Agentic AIOps through the implementation of an Agent2Agent (A2A) communication framework designed to demonstrate automated IT service management. The study investigates how autonomous intelligent agents, developed using LangGraph for workflow orchestration, Model Context Protocol (MCP) for standardized tool integration, and Agent2Agent (A2A) protocol for inter-agent communication, can be applied to automate ITIL v4 practices, specifically focusing on Monitoring and Event Management.

**LangGraph** is a framework for building stateful, multi-actor applications with Large Language Models (LLMs), enabling the creation of complex agent workflows through graph-based state management. It provides sophisticated control flow mechanisms, conditional routing, and persistent state management that allows agents to maintain context across multiple interactions and coordinate complex multi-step operations.

**Model Context Protocol (MCP)** is an open standard that enables secure connections between host applications and external data sources and tools. MCP provides a standardized interface for AI agents to interact with various systems, databases, and APIs while maintaining security boundaries and enabling seamless integration across different platforms and services.

**Agent2Agent (A2A) Protocol** facilitates standardized communication between autonomous agents through well-defined message formats and interaction patterns. A2A enables agents to discover each other's capabilities, exchange structured information, and coordinate complex workflows across distributed systems while maintaining loose coupling and scalability.

## 2. Case Study: ITIL v4 Monitoring and Event Management Practice

### 2.1 Practice Overview

Monitoring and Event Management is a critical ITIL v4 practice that constantly observes services within the organization and records all associated events. These events represent changes of state that impact the product's service delivery capabilities. The practice encompasses continuous surveillance of IT infrastructure, applications, and services to detect deviations from normal operating conditions. Monitoring and Event Management is particularly valuable in identifying information security events and facilitating rapid response with appropriate remediation solutions.

### 2.2 Use Case Context: TechFlow Solutions

*Note: TechFlow Solutions is an invented company used solely to illustrate the use case and demonstrate the practical application of the proposed framework.*

To demonstrate the practical application of Agentic AIOps in ITIL v4 Monitoring and Event Management, this research examines the operational challenges faced by TechFlow Solutions, a mid-sized technology services company operating a cloud-native infrastructure. TechFlow Solutions maintains a production Kubernetes cluster hosting multiple microservices applications that serve over 10,000 daily active users across their e-commerce and customer relationship management platforms.

**Infrastructure Monitoring Scope**: The company's Kubernetes cluster consists of 15 worker nodes running approximately 200 pods across various namespaces including production applications, identity management services, and data processing pipelines. The cluster generates continuous streams of events related to pod lifecycle changes, resource utilization metrics, service health checks, and security alerts that require constant monitoring and analysis.

**Event Management System**: TechFlow Solutions utilizes a centralized service desk web portal for incident and service request management, implementing ITIL v4 best practices for ticket lifecycle management. The portal handles approximately 150-200 tickets per day, ranging from infrastructure alerts and application performance issues to user access requests and change management workflows. Operations staff must manually correlate Kubernetes cluster events with service desk tickets, often leading to delayed incident response and inefficient resource allocation.

**Operational Challenges**: The current manual approach requires dedicated personnel to continuously monitor cluster dashboards, analyze event logs, and create appropriate service desk tickets when issues are detected. This process is prone to human error, suffers from alert fatigue during high-volume periods, and lacks the contextual correlation needed to identify complex multi-system incidents before they impact end users.

### 2.3 Human Complexity Challenges

Traditional human-driven monitoring and event management faces significant complexity challenges that limit operational effectiveness:

**Volume and Velocity Overwhelm**: Modern IT environments generate thousands of events per minute across distributed systems, creating information overload that exceeds human processing capabilities. Operations teams struggle to distinguish critical alerts from routine notifications, leading to alert fatigue and missed incidents.

**Contextual Correlation Complexity**: Events often occur across multiple systems simultaneously, requiring deep technical knowledge to correlate seemingly unrelated alerts into coherent incident patterns. Human operators must maintain extensive mental models of system interdependencies, which becomes increasingly difficult as infrastructure complexity grows.

**24/7 Operational Demands**: Continuous monitoring requires round-the-clock staffing with consistent expertise levels, creating resource constraints and potential coverage gaps during shift transitions or staff unavailability.

**Response Time Pressures**: Critical events demand immediate analysis and response, but human decision-making under pressure can lead to suboptimal choices, delayed responses, or escalation of minor issues into major incidents.

### 2.4 AI-Driven Improvements

AI technologies address these human limitations through intelligent automation and augmentation:

**Intelligent Event Filtering and Prioritization**: Machine learning algorithms analyze historical event patterns to automatically classify and prioritize alerts based on business impact, reducing noise and focusing human attention on truly critical issues.

**Automated Correlation and Root Cause Analysis**: AI systems can process multiple event streams simultaneously, identifying complex correlation patterns across distributed systems that would be impossible for humans to detect manually, enabling faster root cause identification.

**Predictive Analytics**: Advanced algorithms analyze trends and patterns to predict potential failures before they occur, shifting from reactive to proactive monitoring approaches that prevent service disruptions.

**Continuous Learning and Adaptation**: AI systems continuously learn from resolved incidents, improving their accuracy in event classification, correlation, and response recommendations over time without human intervention.

**Autonomous Response Orchestration**: For well-defined scenarios, AI can automatically execute remediation workflows, reducing mean time to resolution and ensuring consistent response procedures regardless of time or staffing levels.

## 3. Proposed Design

The proposed Agentic AIOps framework adopts a specialized agent architecture where each agent is designed to perform a single, well-defined task within the IT operations domain. This design philosophy follows the principle of separation of concerns, enabling each agent to develop deep expertise in its specific operational area while maintaining loose coupling with other system components.

**Specialized Agent Approach**: Each agent in the framework is purpose-built for a specific ITIL practice or operational function. The Kubernetes monitoring agent focuses exclusively on infrastructure oversight and cluster management, while the ticketing agent specializes in incident and service request management. This specialization allows agents to optimize their knowledge base, tool integration, and response patterns for their designated domain, resulting in more accurate and efficient task execution.

**MCP Integration for External Systems**: Agents leverage the Model Context Protocol (MCP) to establish secure, standardized connections with external systems and data sources. MCP provides a unified interface that abstracts the complexity of different APIs and protocols, enabling agents to seamlessly integrate with diverse infrastructure components, monitoring tools, and enterprise systems without requiring custom integration code for each external service.

**A2A Protocol Orchestration**: The Agent2Agent (A2A) protocol serves as the coordination mechanism that enables specialized agents to work together as a cohesive system. Through A2A, agents can discover each other's capabilities, exchange structured messages, and coordinate complex workflows that span multiple operational domains. This orchestration layer maintains agent autonomy while enabling sophisticated multi-agent collaboration patterns.

The framework consists of three primary components that collectively demonstrate these Agentic AIOps principles applied to ITIL v4 practices:

1. **Kubernetes A2A Agent**: Implements infrastructure monitoring and management capabilities through MCP protocol integration for cluster resource oversight
2. **Ticketing A2A Agent**: Provides automated incident and service request management aligned with ITIL ticketing workflows
3. **Agent Host**: Functions as a central orchestration layer that intelligently routes user requests to appropriate specialized agents based on contextual analysis

The implementation leverages LLM for natural language understanding and demonstrates standardized inter-agent communication patterns through A2A protocol integration, enabling seamless coordination between specialized service management agents.

### 3.1 System Architecture

The proposed Agentic AIOps framework implements a distributed multi-agent architecture with the following key components:

**Agent Host (Central Orchestrator)**:
- Implements intelligent request classification using keyword-based routing
- Maintains HTTP connections to specialized agents via A2A protocol
- Provides unified interface for user interactions
- Handles agent discovery and capability resolution
- Routes requests based on contextual analysis of user input

**Kubernetes Monitoring Agent**:
- Integrates with Kubernetes MCP server for real-time cluster monitoring
- Exposes skills for resource monitoring, pod management, and cluster status
- Implements streaming capabilities for continuous monitoring
- Provides RESTful A2A endpoints for inter-agent communication

**Ticketing Service Agent**:
- Connects to ticketing backend via HTTP API
- Implements CRUD operations for ticket management
- Supports ticket creation, querying, and status tracking
- Provides ITIL-compliant incident management workflows

### 3.2 Communication Flow

```
[User Input] → [Agent Host] → [Request Classification] → [Target Agent]
     ↑                                                        ↓
[Response] ← [Response Parsing] ← [A2A Protocol] ← [Agent Processing]
```

**Request Processing Pipeline**:
1. User submits natural language request to Agent Host
2. Agent Host classifies request using keyword matching algorithm
3. Appropriate specialized agent is selected based on classification
4. Request is formatted as A2A protocol message with unique message ID
5. Target agent processes request using LangChain agent executor
6. Response is returned via A2A protocol and parsed for user presentation

### 3.3 Agent Implementation Details

**Kubernetes Agent Architecture**:
- **MCP Integration**: Connects to Kubernetes MCP server on port 8080
- **Tool Loading**: Dynamically loads Kubernetes management tools via MCP
- **Session Management**: Maintains persistent MCP client sessions
- **Error Handling**: Implements robust error handling for MCP connection failures

**Ticketing Agent Architecture**:
- **HTTP API Integration**: Direct REST API calls to ticketing backend on port 5000
- **Tool Registration**: Implements create_ticket, get_all_tickets, and query_tickets tools
- **LangChain Integration**: Uses Gemini LLM with specialized ticketing prompt
- **ITIL Compliance**: Supports standard ITIL incident management processes

**Agent Host Architecture**:
- **Multi-Agent Coordination**: Manages connections to multiple specialized agents
- **Request Classification**: Implements keyword-based routing with fallback logic
- **A2A Client Management**: Maintains A2A clients for each registered agent
- **Async Processing**: Supports asynchronous request processing and response handling

## 4. Solution Implementation

The Agentic AIOps framework is implemented in Python and hosted in a GitHub repository at https://github.com/LuisRubio-zz/unie-aiops. The implementation consists of specialized Python modules that demonstrate the A2A protocol integration with MCP-enabled agents for automated IT service management.

**Project Structure:**
```
unie-aiops/lab2-a2a/
├── src/
│   ├── agent_host.py              # Central orchestration layer
│   ├── k8s_agent_server.py        # Kubernetes A2A agent server
│   ├── k8s_agent_executor.py      # Kubernetes MCP integration logic
│   ├── ticketing_a2a_server.py    # Ticketing A2A agent server
│   └── ticketing_agent_executor.py # Ticketing system integration logic
├── .env.example                   # Environment configuration template
├── pyproject.toml                 # Python project dependencies
└── README.md                      # Implementation documentation
```

### 4.1 Environment Setup and Dependencies

### Clone Repository
```bash
git clone https://github.com/LuisRubio-zz/unie-aiops.git
cd unie-aiops/lab2-a2a/
```

### Environment variables
Get a free gemini api key from https://ai.google.dev/gemini-api/docs/pricing
```bash
# Copy .env template
cp .env.example .env
# Update gemini api key in .env file
vi .env
```

### Setup
```bash
# Install uv:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install dependencies and create virtual environment:
uv sync
```

### 4.2 Agent Deployment

The distributed nature of the Agentic AIOps framework requires each component to be executed in separate Linux terminals to enable concurrent operation and inter-agent communication. This multi-terminal approach allows the ticketing backend, MCP server, specialized agents, and orchestration layer to run simultaneously as independent processes while maintaining A2A protocol connectivity.

#### 4.2.1 Ticketing Service Agent Implementation
The ticketing agent implements ITIL-compliant incident and service request management:

```bash
# In a first terminal start ticketing server at http://localhost:5000
# Note: Use the ticketing server from lab1-agents
cd unie-aiops/lab1-agents/
source .env
uv run python src/ticketing_server.py

# In a second terminal start ticketing A2A agent
cd unie-aiops/lab2-a2a/
source .env
uv run python src/ticketing_a2a_server.py

# Agent will be available at http://localhost:5001
# Agent card at: http://localhost:5001/.well-known/agent
```

#### 4.2.2 Infrastructure Monitoring Agent Implementation
The Kubernetes agent provides automated infrastructure oversight and monitoring capabilities:

```bash
# In a third terminal, download and start k8s MCP server
# Download k8s MCP https://github.com/containers/kubernetes-mcp-server
curl -L -o kubernetes-mcp-server https://github.com/containers/kubernetes-mcp-server/releases/download/v0.0.52/kubernetes-mcp-server-linux-amd64

chmod +x kubernetes-mcp-server

sudo mv kubernetes-mcp-server /usr/bin/

# Load environment variables from .env file:
cd unie-aiops/lab2-a2a/
source .env

kubernetes-mcp-server \
  --port 8080 \
  --kubeconfig ~/.kube/config \
  --sse-base-url http://127.0.0.1:8080 \
  --read-only \
  --log-level 0

# In a fourth terminal start Kubernetes A2A agent
cd unie-aiops/lab2-a2a/
source .env
uv run python src/k8s_agent_server.py

# Agent will be available at http://localhost:8889
# Agent card at: http://localhost:8889/.well-known/agent
```

#### 4.2.3 Orchestration Layer Implementation
The agent host demonstrates intelligent request routing and multi-agent coordination:

```bash
# In a fifth terminal start agent host
cd unie-aiops/lab2-a2a/
source .env
uv run python src/agent_host.py
```

## 5. Results and Validation

The framework demonstrates successful automated request routing and agent coordination:

**Service Request Management:**
```
User Input: "create a ticket for server maintenance"
System Response: "Ticket created successfully"
```

**Infrastructure Query Processing:**
```
User Input: "list the namespaces in my kubernetes cluster"
System Response: "Here are the namespaces in your Kubernetes cluster:
- my-app
- keycloak  
- data-lake"
```

## 6. Discussion

### 6.1 Challenges and Potential Issues

Despite the notable progress of Agentic AIOps technologies in ITIL v4 Monitoring and Event Management, such as improved automation, adaptive decision-making, and dynamic optimization, significant challenges remain, especially in dynamic IT environments characterized by high-volume event streams and complex infrastructure dependencies. Agents often struggle with interpreting evolving operational goals, adapting to changing infrastructure contexts, and processing multi-modal inputs from diverse monitoring sources that influence both high-level service management intentions and low-level technical responses.

Contextual reasoning in monitoring agents requires the ability to process heterogeneous event types from various infrastructure components and leverage domain-specific knowledge for context-aware incident classification—capabilities critical for domains such as security monitoring, performance management, and service availability assurance. Seamless collaboration in ITIL environments demands that Agentic AIOps systems comprehend nuanced service level objectives and operational constraints, requiring not only advanced natural language processing but also deep integration with existing ITSM tools to address complex, unpredictable operational scenarios.

A key tension in Agentic AIOps systems for monitoring and event management is balancing autonomous incident response with human oversight to ensure accurate, transparent, and efficient operations. This becomes increasingly important as agents take on roles that influence service availability and business-critical system stability. The challenge intensifies when agents must distinguish between routine maintenance events and genuine service-impacting incidents, requiring sophisticated pattern recognition and contextual understanding.

To address these limitations in ITIL v4 monitoring contexts, future Agentic AIOps frameworks must integrate real-time adaptability to changing infrastructure patterns, context-aware reasoning for multi-system event correlation, and privacy-preserving mechanisms for sensitive operational data. As IT operations evolve toward more autonomous systems, the emphasis is shifting from pure automation toward human-centric AI collaboration, where optimal partnership between operations teams and monitoring agents is essential for maintaining service quality and operational excellence.

Ethical and operational considerations have long accompanied the evolution of AI in IT operations. Traditionally seen as passive monitoring tools, AI agents in ITIL environments are now becoming collaborative partners that influence and participate in critical operational decision-making processes. Approaching AI ethics in monitoring and event management from this collaborative standpoint requires more than just aligning system outputs with predefined SLAs—it calls for careful design of shared responsibilities between human operators and agents, mechanisms for mutual supervision of incident response actions, and alignment of automated responses with organizational risk tolerance and compliance requirements. Ultimately, building a trustworthy human-AI partnership in ITIL monitoring requires agents to support and enhance operational capabilities while operating under shared ethical principles and maintaining transparency in automated decision-making processes.

## 7. Conclusion

This implementation demonstrates the practical application of AIOps principles in automating ITIL v4 service management practices through intelligent agent coordination. The A2A protocol enables standardized communication between specialized agents, facilitating automated incident management, infrastructure monitoring, and service request fulfillment. Future work should focus on expanding agent capabilities, implementing advanced analytics for predictive maintenance, and integrating additional ITIL processes such as change management and configuration management.

## References

[1] Acharya, D. B., Kuppan, K., & Divya, B. (2025). Agentic AI: Autonomous intelligence for complex goals. *IEEE*. https://ieeexplore.ieee.org/document/10849561

[2] Anthropic. (2024). *Model Context Protocol (MCP)*. Retrieved from https://modelcontextprotocol.io/

[3] LangChain. (2024). *LangGraph: Build language agents as graphs*. Retrieved from https://langchain-ai.github.io/langgraph/

[4] OpenAI. (2024). *Agent2Agent Protocol Specification*. Retrieved from https://github.com/openai/agent2agent

[5] Piccialli, F., Chiaro, D., Sarwar, S., Cerciello, D., Qi, P., & Mele, V. (2025). AgentAI: A comprehensive survey on autonomous agents in distributed AI for industry 4.0. Retrieved from https://www.sciencedirect.com/science/article/pii/S0957417425020238?via%3Dihub