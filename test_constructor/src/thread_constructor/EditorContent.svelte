<script>
    export let data;
</script>


<div class="editor-content">
  {#each data.blocks as block}
    {#if block.type === 'paragraph'}
      <p>
        {@html block.data.text}
      </p>
    {/if}
    {#if block.type === 'list'}
      {#if block.data.style === 'ordered'}
        <ol>
          {#each block.data.items as item}
            <li>{@html item}</li>
          {/each}
        </ol>
      {:else}
        <ul>
          {#each block.data.items as item}
            <li>{@html item}</li>
          {/each}
        </ul>
      {/if}
    {/if}
    {#if block.type === 'image'}
      <img src="{block.data.file.url}" alt="">
      <p class="caption">{block.data.caption}</p>
    {/if}
    {#if block.type === 'embed'}
      {#if block.data.service === 'youtube'}
        <iframe width="100%" height="315" src="{ block.data.embed }" title="YouTube video player"
                frameborder="0"
                allowfullscreen></iframe>
      {/if}
      <p class="caption">{block.data.caption}</p>
    {/if}
  {/each}
</div>

<style>
    .editor-content {
        cursor: pointer;
        transition: all .3s ease;
        border-radius: 15px;
        padding: 15px;
        margin: 0 -15px;
    }

    .editor-content:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }

    img {
        max-width: 100%;
        max-height: 400px;
    }

    .caption {
        width: 100%;
        text-align: center;
        opacity: .5;
    }
</style>