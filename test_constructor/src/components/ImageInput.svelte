<script>
    import Input from './Input.svelte';
    export let name = '';
    export let value;
</script>

<Input type="image" {name} bind:value/>
