<script>
    export let text;
    export let value;
    export let choices;
</script>

<div>
  <p>{text}</p>
  <select bind:value>
    {#each choices as choice}
      <option value={choice.name}>
        {choice.label}
      </option>
    {/each}
  </select>
</div>

<style>
  select {
      width: 100%;
  }
</style>