from typing import Literal

ResponseFormatT = Literal["dom", "plain", "html"]
ScopeOptionT = Literal["me", "create_annotation", "manage_annotation", "vote"]
ScopeT = tuple[ScopeOptionT, ...] | Literal["all"]
TextFormatT = Literal["dom", "html", "markdown", "plain"]
