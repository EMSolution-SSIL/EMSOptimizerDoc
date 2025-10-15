import Heading from '@theme/Heading';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: '幅広い形状最適化手法のサポート',
    Svg: require('@site/static/img/shape_optimization.svg').default,
    description: (
      <>
        EMSOptimizerはon/off法ベースのトポロジー最適化手法を内蔵しており、特に電気機器の概念設計のフェーズにおいて威力を発揮します。
        また、モータ設計およびシミュレーションツール「eMotorSolution」との連携によりモータのパラメータ最適化を、さらにはパラメータとトポロジーの同時最適化まで実現可能です。
        最適化手法は単目的・多目的両方をサポート。実用上重要な制約条件の取り扱いも柔軟です。
      </>
    ),
  },
  {
    title: 'Python製ソフトウェアの柔軟性',
    Svg: require('@site/static/img/python-logo-only.svg').default,
    description: (
      <>
        EMSOptimizerはPythonプログラミング言語製の一部公開ソフトウェアです。
        基本の最適化設定はコンフィグファイルのみで完結する一方で、
        独自の最適化アルゴリズムや形状関数を設定したいユーザはPython製プラグインを作成し、EMSOptimizerと直接連携させることが可能。
        ユーザの研究開発をサポートします。
      </>
    ),
  },
  {
    title: 'EMSolutionの力を活用',
    Svg: require('@site/static/img/emsol.svg').default,
    description: (
      <>
        形状最適化には、複雑かつ高効率な形状解析が必要です。EMSOptimizerは、強力かつ高効率なシミュレーションエンジンであるEMSolutionによって駆動されています。
        EMSolutionはPythonにバインドされており（pyemsol）、EMSOptimizerの最適化アルゴリズムと連携することで効率的な形状最適化を実現します。
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
