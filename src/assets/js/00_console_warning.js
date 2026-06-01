(() => {
    const titleStyle = [
        'color: #ff3b30',
        'font-size: 48px',
        'font-weight: 900',
        'line-height: 1.2',
        'text-shadow: 1px 1px 0 #000'
    ].join(';');

    const messageStyle = [
        'color: #f5f5f5',
        'font-size: 16px',
        'line-height: 1.5'
    ].join(';');

    const brandStyle = [
        'color: #00bcd4',
        'font-size: 18px',
        'font-weight: 700'
    ].join(';');

    console.log('%c¡Detente!', titleStyle);

    console.log(
        '%cEsta consola del navegador está pensada solo para desarrolladores. ' +
        'Si alguien te indicó copiar, pegar o modificar código aquí para habilitar una función, ' +
        'solucionar un error o acceder a información, podría tratarse de un fraude o una acción riesgosa.',
        messageStyle
    );

    console.log(
        '%cADA: cualquier cambio ejecutado desde esta consola puede afectar el funcionamiento de la página, ' +
        'alterar datos visibles, interrumpir procesos o comprometer tu sesión.',
        brandStyle
    );

    console.log(
        '%cSi no sabes exactamente qué hace un comando, no lo ejecutes.',
        messageStyle
    );
})();