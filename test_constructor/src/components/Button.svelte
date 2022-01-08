<script>
    export let text;
    export let callback;
    export let className = '';
</script>

<button on:click={callback} class="{className}">
  {text}
</button>

<style>
    button {
        --color: var(white);
        --border-color: rgba(0, 0, 0, .1);
        position: relative;
        opacity: 0.5;
        border-radius: 10px;
        padding: 10px;
        cursor: pointer;
        z-index: 2;
        width: 100%;
        border: var(--border);
        background-color: var(--color);
        border-color: var(--border-color);
    }

    button.success {
        --color: var(--test-correct-background);
        --border-color: var(--test-correct-text);
        color: var(--test-correct-text);
    }

    button.danger {
        --color: white;
        --border-color: var(--live);
        color: var(--live);
    }

    button.test {
        --color: white;
        --border-color: var(--test);
        color: var(--link-test);
    }

    button:before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        left: -1px;
        top: -1px;
        z-index: -1;
        border-radius: 10px;
        border: var(--border);
        opacity: 0;
        background-color: rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }

    button:hover:before {
        opacity: 1;
    }

    button:active:before {
        background-color: rgba(255, 255, 255, 0.15);
    }
</style>