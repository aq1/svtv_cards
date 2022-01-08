<script>
    export let name = '';
    export let type = 'text';
    export let placeholder = '';
    export let value;
</script>

<div>
  {#if name}
    <div>{name}</div>
  {/if}
  {#if type === 'text'}
    <input type="text" bind:value={value} {placeholder}>
  {:else if type === 'image'}
    <input type="file" bind:value={value} accept="image/*">
  {/if}
</div>

<style>
    div {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    input {
        width: 100%;
        border: none;
        transition: all .3s ease;
    }

    input[type="text"] {
        border-bottom: var(--border);
        padding: 10px;
    }

    input:focus-visible {
        outline: none;
        border-bottom-color: var(--background-3);
        box-shadow: none;
    }
</style>