import { Fragment } from "react";
import YouTube from 'react-youtube';
const imageServer = "http://hoangpnapi2.hungphu.org"

const Sidebar = ({ dataFromClick, widthDynamic }) => {
    const styleMap = {
        // top: 70,
        left: 0,
        width: widthDynamic,
        height: "100%",
        position: "absolute",
        backgroundColor: "white",
        overflow: 'hidden'
    }; ``
    const opts = {
        position: 'relative',

        width: '100%',
        playerVars: {
          // https://developers.google.com/youtube/player_parameters
          autoplay: 1,
        },
      };
    return (
        <Fragment>
            <div style={styleMap}>
                <img
                // src={`https://images.unsplash.com/photo-1516802273409-68526ee1bdd6`}
                src={`${imageServer}${dataFromClick.image_path}`}
                // src={item.img}
                // src={'http://localhost:5003/3Batch_KeyFrames/KeyFramesC02_V00/C02_V0021/013729.jpg'}
                // srcSet={`${item.img}?w=164&h=164&fit=crop&auto=format&dpr=2 2x`}
                // alt={item.title}
                loading="lazy"
                style={{width:"100%"}}
                />
                <YouTube videoId={`${dataFromClick.id_video}`}
                    opts={opts}
                />
            </div>
        </Fragment>
    );
};

export default Sidebar;
// dòng số 6 muốn cho nó ẩn thì set biến động cho nó về 0 khi nào ấn click thì cho biến đó tăng lên
// dòng số 16 tự css nha
