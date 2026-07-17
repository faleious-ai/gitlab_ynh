# Assurance da arquitetura de trabalho v2

A revisão adversarial de RND-015 foi convertida em requisitos executáveis:

- backlog fora da queue impede falso stop;
- finding aberto exige correção;
- proteção usa diff Git real e hashes;
- ownership é prefix-aware;
- lanes exigem workers, overlap, artifact e log hashados;
- task só conclui por receipt SELF publicado;
- review/ambiente são checkpoint, não conclusão;
- coverage T1–T8/WP-00–WP-09 é verificada por `doctor`.

A arquitetura foi validada no sandbox a partir dos ZIPs fornecidos pelo usuário. A publicação remota usa commits atômicos e fast-forward sem force.
