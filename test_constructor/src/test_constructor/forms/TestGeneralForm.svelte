<script>
    import Input from '../../components/Input.svelte';
    import Select from '../../components/Select.svelte';
    import Card from '../../components/Card.svelte';
    import ImageInput from '../../components/ImageInput.svelte';
    import {TEST_TYPES} from '../default-test-values';

    export let data;
</script>

<Card>
  <ImageInput bind:value={data.cover}/>
  <Select bind:value={data.type} choices={TEST_TYPES} text="Тип теста"/>
  <Input bind:value={data.title} placeholder="Название"/>
  <Input bind:value={data.slug} placeholder="Slug в ссылке"/>
  <Input bind:value={data.description} placeholder="Короткое описание"/>
</Card>
