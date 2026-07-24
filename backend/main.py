from	fastapi	import	FastAPI
from	audit.schemas	import	AuditRequest,	AuditResponse
from	audit.scoring	import	compute_trust_score
app	=	FastAPI(title="TrustAudit	AI",	version="0.1.0")
@app.get("/")
def	read_root():
 return	{"message":	"TrustAudit	AI	backend	is	running."}
@app.get("/health")
def	health_check():
 return	{"status":	"ok"}
@app.post("/audit",	response_model=AuditResponse)
def	audit_text(request:	AuditRequest):
 result	=	compute_trust_score(request.text)
 return	result