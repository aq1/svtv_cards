<script>
    import Button from '../../components/Button.svelte';
    import Card from '../../components/Card.svelte';
    import {getTest} from '../default-test-values';

    export let tests = [];
    export let test = [];

    const selectTest = (selectedTest) => () => {
       test = selectedTest || getTest();
    };

</script>

<Card>
  <Button text="Новый тест" className="test" callback={selectTest()}/>
  {#each tests as test}
    <Button text="{test.general.title}" callback={selectTest(test)}/>
  {/each}
</Card>
