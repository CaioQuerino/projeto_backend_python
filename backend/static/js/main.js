document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formCadastro');
    const mensagem = document.getElementById('mensagem');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/api/clientes', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                const successStyle = 'background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;';
                const errorStyle = 'background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;';
                
                mensagem.innerHTML = `<div style="padding: 10px; margin: 10px 0; border-radius: 5px; ${data.success ? successStyle : errorStyle}">
                    ${data.message}
                </div>`;
                
                if (data.success) {
                    this.reset();
                    
                    setTimeout(() => {
                        mensagem.innerHTML = '';
                    }, 5000);
                }
            } catch (error) {
                mensagem.innerHTML = `<div style="padding: 10px; margin: 10px 0; border-radius: 5px; background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;">
                    Erro ao enviar formulário. Tente novamente.
                </div>`;
                
                console.error('Erro:', error);
            }
        });
    }
});