<script>
    import Button from '../../components/Button.svelte';
    import Card from '../../components/Card.svelte';
    import TestResultField from '../fields/TestResultField.svelte';
    import {getResult} from '../default-test-values';

    export let results;

    const addResult = () => {
        results = [
            ...results,
            getResult(),
        ];
    };
    const deleteResult = (index) => () => {
        results = [...results.slice(0, index), ...results.slice(index + 1, results.length)];
    }
</script>

<div class="wrapper">
  {#each results as result, index}
    <Card>
      <div class="header">
        <div class="header__text">
          Результат {index + 1} / {results.length}
        </div>
        <div class="header__button">
          <Button text="-" callback={deleteResult(index)} className="danger"/>
        </div>
      </div>
      <TestResultField bind:result/>
    </Card>
  {/each}
  <Button text="+ результат" callback={addResult}/>
</div>

<style>
    .wrapper {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .header {
        display: flex;
        justify-content: space-between;
    }

    .header__text {
        flex: 1 1 70%;
    }

    .header__button {
        width: 36px;
    }
</style>
