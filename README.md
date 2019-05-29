<h1>PayBot Whats'App</h1>
<p> Um bot de cobrança por whats'App </p>
<h2> O que é o Projeto </h2>
<p> O PayBot Whats'App tem intuito inicial de extrair e tratar nomes do pdf do Banco Santander, pesquisá-lo nos contatos e enviar uma mensagem padrão.</p>

<h2> Principais Funcionalidades </h2>
<h3> Busca de contatos </h3>
<p> O comando find_contacts insere o nome passado no parametro.<br> <b>Obs: se o contato nao for encontrado, ele retorna False</b></p>
<img src="./images/lblSearch.png"/>
<h3> Envio de Mensagens </h3>
<p> O comando send_message envia a mensagem passada no parametro, e enviá-la para o contato da tela atual.<br>É opcional escolher o contato, caso escolha ocorrerá a chamada de Busca de Contatos</p>
<img src="./images/MessageArea.png"/>
<h3> Cobrança </h3>
<p> Comando Especial que lê o pdf de cobrança do Banco Santander, extrai os nomes , busca contatos com esses nomes e envia uma mensagem padrão</p>
<h2> Diário de bordo</h2>
<h2> Dia 29/05/2019 </h2>
Neste dia eu fiz:
<ul>
  <li>Implementação do Xpath no PO</li>
  <li>Atualização do PO</li>
</ul>
<p>Obtive algumas dificuldade na inserção do nome de contato na label de procura, tentei executar um comando javascript, porem com falhas,dessa forma utilizei um metodo do proprio selenium</p>
