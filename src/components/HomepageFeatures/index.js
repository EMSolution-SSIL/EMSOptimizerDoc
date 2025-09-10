import Heading from '@theme/Heading';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: '幅広い形状最適化手法のサポート',
    Svg: require('@site/static/img/shape_optimization.svg').default,
    description: (
      <>
        EMOptSolutionでは、on/off法ベースのトポロジー最適化を採用しており、特に概念設計のフェーズにおいて威力を発揮します。
        また、モータ設計およびシミュレーションツール「eMotorSolution」との連携によりモータの寸法最適化を、さらには寸法とトポロジーの同時最適化まで実現可能です。
        最適化手法は単目的・多目的両方をサポート。実用上重要な制約条件の取り扱いも柔軟です。
      </>
    ),
  },
  {
    title: '使いやすさとカスタマイズ性の両立',
    Svg: require('@site/static/img/usability.svg').default,
    description: (
      <>
        基本的に最適化設定はコンフィグファイルのみで完結。
        一方、独自の最適化アルゴリズムや形状関数を設定したいユーザはpythonによってプラグインを作成し、EMOptSolutionと直接連携させることができます。
        プラグインは純粋なpythonのインターフェースとして定義されており、容易に拡張が可能。ユーザの研究開発をサポートします。
      </>
    ),
  },
  {
    title: 'EMSolutionの力を活用',
    Svg: require('@site/static/img/emsol.svg').default,
    description: (
      <>
        形状最適化には、複雑かつ高効率な計算が必要です。EMOptSolutionは、強力かつ高効率なシミュレーションエンジンであるEMSolutionによって駆動されています。
        EMSolutionはPythonにバインドされており、EMOptSolutionの最適化アルゴリズムと併せることで効率的な形状最適化を実現します。
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
