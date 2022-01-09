<script>
    import Input from '../../components/Input.svelte';
    import ImageInput from '../../components/ImageInput.svelte';

    export let result;
</script>

<div>
  <ImageInput bind:value={result.image}/>
  <Input bind:value={result.header} placeholder="Заголовок"/>
  <Input bind:value={result.text} placeholder="Небольшой текст"/>
  <Input bind:value={result.shareUrl} placeholder="Slug ссылки для шеринга"/>
</div>

<style>
  div {
      display: flex;
      flex-direction: column;
      gap: 10px;
  }
</style>