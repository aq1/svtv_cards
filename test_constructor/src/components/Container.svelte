<div>
  <slot></slot>
</div>

<style>
    div {
        width: 100vw;
        padding: 30px;
    }

    @media screen and (min-width: 860px) {
        div {
            width: 45vw;
            margin: 0 auto;
        }
    }
</style>