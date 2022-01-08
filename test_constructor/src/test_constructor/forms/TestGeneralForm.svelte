<script>
    import Input from '../../components/Input.svelte';
    import Card from '../../components/Card.svelte';
    import ImageInput from '../../components/ImageInput.svelte';

    export let data;
</script>

<Card>
  <ImageInput bind:value={data.cover}/>
  <Input bind:value={data.title} placeholder="Название"/>
  <Input bind:value={data.description} placeholder="Короткое описание"/>
</Card>

